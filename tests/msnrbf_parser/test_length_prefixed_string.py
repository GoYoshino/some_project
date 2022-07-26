import unittest

from underrail_translation_kit.msnrbf_parser.primitives import LengthPrefixedString
from .helper import assertEndOfStream, assertEqualToStream

class LengthPrefixedStringTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("msnrbf_parser/data/string", "rb") as stream:
            obj = LengthPrefixedString.from_stream(stream)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

        self.assertEqual(obj.string, "This is the internal currency of the South Gate Station.")
        self.assertEqual(obj.length, 56)

    def test_works_on_loooong_text(self):
        with open("msnrbf_parser/data/uirou_uri", "rb") as stream:
            obj = LengthPrefixedString.from_stream(stream)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

        with open("msnrbf_parser/data/uirou_uri.txt", "r", encoding="utf-8") as stream:
            self.assertEqual(obj.string, stream.read())
            self.assertEqual(obj.length, 2934)

if __name__ == '__main__':
    unittest.main()
