from fnmatch import fnmatch
import os
from typing import List, Tuple

# now constant for development. will be command line in future
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
                if fnmatch(fn, target):
                    file_list.append((root, name))

    return file_list