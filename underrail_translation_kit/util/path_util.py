from fnmatch import fnmatch
import os
from pathlib import Path
from typing import List, Tuple

def list_all_files(data_dir: str, targets: List[str]) -> List[str]:
    file_list = []
    for root, dirs, files in os.walk(data_dir, topdown=False):
        for name in files:
            for target in targets:
                fn = os.path.join(root, name)
                if fnmatch(fn, target):
                    file_list.append(fn)

    return file_list

def get_relative_path_from_data(path: Path) -> Path:
    index_of_data = -1
    for i, part in enumerate(path.parts):
        if part == "data":
            index_of_data = i
            break
    return Path("/".join(path.parts[index_of_data + 1:]))