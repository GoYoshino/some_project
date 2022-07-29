import unittest

from underrail_translation_kit.msnrbf_parser.length_prefixed_string import LengthPrefixedString
from tests.msnrbf_parser.helper import assertEndOfStream, assertEqualToStream

class LengthPrefixedStringTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("msnrbf_parser/data/string", "rb") as stream:
            obj = LengthPrefixedString.from_stream(stream)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

        self.assertEqual(obj.string, "This is the internal currency of the South Gate Station.")
        self.assertEqual(obj.string_byte_length, 56)

    def test_works_on_loooong_text(self):
        with open("msnrbf_parser/data/uirou_uri", "rb") as stream:
            obj = LengthPrefixedString.from_stream(stream)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

        with open("msnrbf_parser/data/uirou_uri.txt", "r", encoding="utf-8") as stream:
            uirou = stream.read()
            self.assertEqual(obj.string, uirou)
            self.assertEqual(obj.string_byte_length, len(uirou.encode("utf-8")))

    def test_direct_generation(self):
        obj = LengthPrefixedString.from_value("abcdefgggg")
        self.assertEqual("abcdefgggg", obj.string)
        self.assertEqual(len("abcdefgggg".encode("utf-8")), obj.string_byte_length)
        self.assertEqual(b"\x0Aabcdefgggg", obj.raw_bytes)

if __name__ == '__main__':
    unittest.main()
