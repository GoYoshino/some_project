import json
import os
from pathlib import Path
from typing import List, Dict

from underrail_translation_kit.unpacker import unpack_as_stream
from underrail_translation_kit.msnrbf_parser import ParseResult, parse_binary_stream
from underrail_translation_kit.util import list_all_files, get_relative_path_from_data

# now constant for development. will be command line in future
UNDERRAIL_DATA_DIR = Path(r"D:\SteamLibrary\steamapps\common\Underrail\backup\data")
JSON_OUT_DIR = Path("D:/underrail_json/data")

TARGETS = [
    "*.k",
    "*.item"
]

def generate_json_dictionary(class_name: str, object_id: int, original_text: str, description: str) -> Dict[str, str]:
    return {
        "className": class_name,
        "objectId": object_id,
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
            class_name = class_.get_name()

            member = members[member_key]
            object_id = member.get_object_id()

            json_dict = generate_json_dictionary(class_name, object_id, member.get_string(), "n/a")

            json_dict_list.append(json_dict)

    return json_dict_list

def load_object(filepath: str) -> ParseResult:
    with unpack_as_stream(filepath) as f:
        return parse_binary_stream(f)



if __name__ == "__main__":
    os.sep = "/"

    all_files = list_all_files(UNDERRAIL_DATA_DIR, TARGETS)

    for file in all_files:
        path = Path(file[0] + "/" + file[1])
        relative_path = get_relative_path_from_data(path)

        print(f"processing {path}")
        save_dir = os.path.join(JSON_OUT_DIR, relative_path.parent)
        os.makedirs(save_dir, exist_ok=True)

        obj = load_object(path)
        json_data = generate_whole_extract_json(obj)

        save_path = str(JSON_OUT_DIR.joinpath(relative_path)) + ".json"
        print(save_path)
        with open(save_path, "w") as f:
            json.dump(json_data, f, indent=4)