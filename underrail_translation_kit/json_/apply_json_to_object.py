import json
import os
from pathlib import Path
from typing import List, Dict

from underrail_translation_kit.msnrbf_parser import ParseResult, parse_binary_stream
from underrail_translation_kit.util import list_all_files, get_relative_path_from_data
from underrail_translation_kit.unpacker import unpack_as_stream, to_underrail_gzip

JSON_DIR = Path("D:/underrail_json_X")
UNDERRAIL_DATA_DIR = Path(r"D:\SteamLibrary\steamapps\common\Underrail\data")
TARGETS = [
    "*.json"
]

def load_object(filepath: str) -> ParseResult:
    with unpack_as_stream(filepath) as f:
        return parse_binary_stream(f)

def save_object(object_: ParseResult, filepath: str):
    with open(filepath, "rb") as f:
        header = f.read(24)
    gzip_bytes = to_underrail_gzip(object_.raw_bytes, header)
    with open(filepath, "wb") as f:
        f.write(gzip_bytes)

def apply_json_to_object(object: ParseResult, json_data: List[Dict[str, str]]):
    """
    warning: does change object state
    :param object:
    :param json_data:
    :return:
    """

    for data in json_data:

        # Does nothing translatedText is empty(to avoid breaking key)
        if data["translatedText"] == "":
            continue

        object.replace_text(data["translatedText"], data["targetPath"])

if __name__ == "__main__":
    all_files = list_all_files(JSON_DIR, TARGETS)



    for file in all_files:
        json_path = Path(file[0] + "/" + file[1])
        relative_path = get_relative_path_from_data(json_path)

        print(f"processing {json_path}")
        with open(json_path, "r", encoding="utf-8") as f:
            json_object = json.load(f)

        ul_file_path = os.path.join(UNDERRAIL_DATA_DIR, str(relative_path))[:-5]
        original_obj = load_object(ul_file_path)

        apply_json_to_object(original_obj, json_object)
        #print(object.raw_bytes)

        save_object(original_obj, ul_file_path)
