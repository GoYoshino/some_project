import json
import fnmatch
import os
from pathlib import Path
from typing import List, Tuple, Dict

from underrail_translation_kit.json_.annotation import add_annotation
from underrail_translation_kit.unpacker import unpack_as_stream
from underrail_translation_kit.msnrbf_parser import ParseResult, parse_binary_stream

# now constant for development. will be command line in future
UNDERRAIL_DATA_DIR = Path(r"D:\SteamLibrary\steamapps\common\Underrail\backup\data")
JSON_OUT_DIR = Path("D:/underrail_json")

TARGETS = [
    "*.k",
    "*.item"
]

def list_all_files(data_dir: str) -> List[Tuple[str, str]]:
    file_list = []
    for root, dirs, files in os.walk(data_dir, topdown=False):
        for name in files:
            for target in TARGETS:
                fn = os.path.join(root, name)
                if fnmatch.fnmatch(fn, target):
                    file_list.append((root, name))

    return file_list

def generate_json_dictionary(target_path: str, original_text: str, description: str) -> Dict[str, str]:
    return {
        "targetPath": target_path,
        "description": description,
        "originalText": original_text,
        "translatedText": ""
    }

def generate_whole_extract_json(obj: ParseResult) -> List[Dict[str, str]]:
    json_dict_list = []

    classes = obj.get_all_member_class()
    for key in classes:
        class_ = classes[key]
        members = class_.get_string_member_dict()
        for member_key in members:
            member = members[member_key]
            path = f"{key}.{member_key}"
            json_dict = generate_json_dictionary(path, member.get_string(), "not available (whole extraction)")
            add_annotation(json_dict)

            json_dict_list.append(json_dict)

    return json_dict_list

def load_object(filepath: str) -> ParseResult:
    with unpack_as_stream(filepath) as f:
        return parse_binary_stream(f)

def get_relative_path_from_data(path: Path) -> Path:
    index_of_data = -1
    for i, part in enumerate(path.parts):
        if part == "data":
            index_of_data = i
            break
    return Path("/".join(path.parts[index_of_data:]))

if __name__ == "__main__":
    os.sep = "/"

    all_files = list_all_files(UNDERRAIL_DATA_DIR)

    for file in all_files:
        path = Path(file[0] + "/" + file[1])
        relative_path = get_relative_path_from_data(path)

        print(f"processing {path}")
        save_dir = os.path.join(JSON_OUT_DIR, relative_path.parent)
        os.makedirs(save_dir, exist_ok=True)

        obj = load_object(path)
        json_data = generate_whole_extract_json(obj)

        save_path = JSON_OUT_DIR.joinpath(relative_path)
        save_path = os.path.splitext(str(save_path))[0] + ".json"
        print(save_path)
        with open(save_path, "w") as f:
            json.dump(json_data, f, indent=4)