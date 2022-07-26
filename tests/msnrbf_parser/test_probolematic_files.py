import unittest

from underrail_translation_kit.msnrbf_parser import parse_binary_stream
from tests.msnrbf_parser.helper import assertEqualToStream

""""
単体テストではないが、
過去、特に問題を引き起こしたファイルを読んでテストする
"""

class ProbolematicFilesTest(unittest.TestCase):

    def test_read_item_file(self):
        with open("msnrbf_parser/data/sgscredits", "rb") as f:
            result = parse_binary_stream(f)
            assertEqualToStream(self, result.raw_bytes, f)

    def test_read_item_file2(self):
        with open("msnrbf_parser/data/stygiancoin", "rb") as f:
            result = parse_binary_stream(f)
            assertEqualToStream(self, result.raw_bytes, f)

    def test_read_knowledge_file(self):
        with open("msnrbf_parser/data/baseabilities", "rb") as f:
            result = parse_binary_stream(f)
            assertEqualToStream(self, result.raw_bytes, f)

if __name__ == '__main__':
    unittest.main()
