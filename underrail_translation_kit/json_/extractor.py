import json
import os
from pathlib import Path
from typing import List, Dict

from underrail_translation_kit.unpacker import unpack_as_stream
from underrail_translation_kit.msnrbf_parser import ParseResult, parse_binary_stream
from underrail_translation_kit.json_.postprocess import postprocess
from underrail_translation_kit.util import list_all_files, UnderrailPath

TARGETS = [
    "*.udlg",
    "*.k",
    "*.item"
]

def __generate_json_dictionary(class_name: str, object_id: int, original_text: str, description: str) -> Dict[str, str]:
    return {
        "className": class_name,
        "objectId": object_id,
        "description": description,
        "originalText": original_text,
        "translatedText": ""
    }

def __extract_from_a_object(obj: ParseResult) -> List[Dict[str, str]]:
    json_dict_list = []

    texts = obj.get_all_texts()
    for index in texts:
        text = texts[index]
        object_id = text.get_object_id()

        json_dict = __generate_json_dictionary("", object_id, text.get_string(), "n/a")

        json_dict_list.append(json_dict)

    return json_dict_list

def __load_object(filepath: str) -> ParseResult:
    with unpack_as_stream(filepath) as f:
        return parse_binary_stream(f)

def extract(underrail_root: str, json_root: str, dry_mode=True):
    # data側のファイルをカウントする
    paths_raw = list_all_files(underrail_root, TARGETS)

    paths = [UnderrailPath(path, underrail_root, json_root) for path in paths_raw]

    for i, path in enumerate(paths):
        print(f"{path.datafile()} => {path.json()}...({i + 1}/{len(paths)})")
        object = __load_object(path.datafile())
        json_data = __extract_from_a_object(object)
        json_data = postprocess(json_data)

        if not dry_mode:
            os.makedirs(path.json_dir(), exist_ok=True)
            with open(path.json(), "w") as f:
                json.dump(json_data, f, indent=4)

if __name__ == "__main__":
    # (※使用例)
    #UNDERRAIL_DATA_DIR = Path(r"D:\SteamLibrary\steamapps\common\Underrail\data")
    UNDERRAIL_DATA_DIR = Path(r"D:\underrail_jp_full\data\underrail_master\data")
    JSON_OUT_DIR = Path(r"D:\underrail_json_test\data")
    extract(UNDERRAIL_DATA_DIR, JSON_OUT_DIR, False)