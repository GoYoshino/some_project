import unittest

from decode import decode
from tests.helpers.bytes_asserts import assertEqualToStream

class ReadWholeFileTest(unittest.TestCase):

    def test_read_item_file(self):
        with open("data/sgscredits", "rb") as f:
            result = decode(f)
            assertEqualToStream(self, result.raw_bytes, f)

    def test_read_item_file2(self):
        with open("data/stygiancoin", "rb") as f:
            result = decode(f)
            assertEqualToStream(self, result.raw_bytes, f)

    def test_read_knowledge_file(self):
        with open("data/baseabilities", "rb") as f:
            result = decode(f)
            assertEqualToStream(self, result.raw_bytes, f)

if __name__ == '__main__':
    unittest.main()
