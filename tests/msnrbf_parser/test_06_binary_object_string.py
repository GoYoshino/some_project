import unittest

from underrail_translation_kit.msnrbf_parser.primitives import Int8
from underrail_translation_kit.msnrbf_parser.binary_object_string import BinaryObjectString
from .helper import assertEndOfStream, assertEqualToStream

class BinaryObjectStringTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("msnrbf_parser/data/06_BinaryObjectString", "rb") as stream:
            header = Int8.from_stream(stream)
            self.assertEqual(header.raw_bytes, b"\x06")
            obj = BinaryObjectString.from_stream(stream)
            self.assertEqual(obj.get_string(), "currency.sgs")
            self.assertEqual(obj.get_length(), 12)

            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

if __name__ == '__main__':
    unittest.main()
