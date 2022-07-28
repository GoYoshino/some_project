"""
全てのunderrailファイルに対して読み込みの整合性をチェックする
単体テストのように常に走らせる類のものではないことに注意
"""

import traceback
import tqdm

from underrail_translation_kit.msnrbf_parser import parse_binary_stream
from underrail_translation_kit.unpacker import unpack_as_stream
from underrail_translation_kit.util import list_all_files

underrail_master_dir = "../../data/underrail_master/data"

if __name__ == "__main__":

    files = list_all_files(underrail_master_dir, ["*.item", "*.udlg", "*.k"])

    print(f"testing {len(files)} files..")

    corrupt_count = 0
    for i in tqdm.tqdm(range(len(files))):
        file = files[i]
        with unpack_as_stream(file) as stream:
            try:
                object_ = parse_binary_stream(stream)
                stream.seek(0)
                file_raw_bytes = stream.read()
                if not object_.raw_bytes == file_raw_bytes:
                    print(f"Raw bytes does not match at {file}:")
                    print(f"OBJ:{object_.raw_bytes}")
                    print(f"DAT:{file_raw_bytes}")
                    print(object_)
                    corrupt_count += 1
            except Exception:
                print(f"Exception at {file}")
                print(traceback.format_exc())

    print(f"done. {corrupt_count} files are corrupted.")