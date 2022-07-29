import json
import os
from pathlib import Path
from typing import List, Dict

from underrail_translation_kit.msnrbf_parser import ParseResult, parse_binary_stream
from underrail_translation_kit.util import list_all_files, UnderrailPath
from underrail_translation_kit.unpacker import unpack_as_stream, to_underrail_gzip


TARGETS = [
    "*.json"
]

def __load_object(filepath: str) -> ParseResult:
    with unpack_as_stream(filepath) as f:
        return parse_binary_stream(f)

def __save_gzip_object(object_: ParseResult, filepath: str, header: bytes):
    assert len(header) == 24
    gzip_bytes = to_underrail_gzip(object_.raw_bytes, header)
    with open(filepath, "wb") as f:
        f.write(gzip_bytes)

def __save_raw_object(object_: ParseResult, filepath: str, header: bytes):
    assert len(header) == 24
    with open(filepath, "wb")as f:
        f.write(header)
        f.write(object_.raw_bytes)

def __apply_json_to_object(object: ParseResult, json_data: List[Dict[str, str]]):
    """
    warning: does change object state
    :param object:
    :param json_data:
    :return:
    """

    for data in json_data:

        # ignores jsonversion
        if "jsonVersion" in data:
            continue

        # Does nothing translatedText is empty(to avoid breaking key)
        if data["translatedText"] == "":
            continue

        object.replace_text(data["translatedText"], int(data["objectId"]))

def patch(underrail_root: str, json_root: str, patch_root: str, dry_mode:bool=True):
    # json側のファイルをカウントする
    # (まだ適用したくないJSONは消しておくことができるように)
    paths_raw = list_all_files(json_root, TARGETS)

    paths = [UnderrailPath(path, underrail_root, json_root, patch_root) for path in paths_raw]

    for i, path in enumerate(paths):
        print(f"{path.datafile()} + {path.json()}\n=>{path.patch()}...({i + 1}/{len(paths)})")
        with open(path.json(), "r", encoding="utf-8") as f:
            json_object = json.load(f)

        underrail_bin = __load_object(path.datafile())
        __apply_json_to_object(underrail_bin, json_object)

        with open(path.datafile(), "rb") as f:
            header = f.read(24)
            magic = f.read(2)

        if dry_mode:
            print(underrail_bin)
        else:
            os.makedirs(path.patch_dir(), exist_ok=True)
            if magic == b"\x1F\x8B":
                __save_gzip_object(underrail_bin, path.patch(), header)
            else:
                __save_raw_object(underrail_bin, path.patch(), header)

if __name__ == "__main__":
    # 使用例
    JSON_DIR = Path(r"G:/underrail_json_test\data")
    UNDERRAIL_DATA_DIR = Path(r"G:\SteamLibrary\steamapps\common\Underrail\data")
    PATCH_OUT_DIR = Path(r"G:\underrail_patch\data")

    patch(UNDERRAIL_DATA_DIR, JSON_DIR, PATCH_OUT_DIR, False)