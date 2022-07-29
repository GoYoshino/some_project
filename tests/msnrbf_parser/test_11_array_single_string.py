import unittest

from underrail_translation_kit.msnrbf_parser.misc_record_classes import ArraySingleString
from underrail_translation_kit.msnrbf_parser.primitives import Int8
from .helper import assertEndOfStream, assertEqualToStream

class ArraySingleStringTest(unittest.TestCase):

    def test_fabricate(self):
        pass

    def test_reading_stream(self):
        with open("msnrbf_parser/data/11_ArraySingleString", "rb") as stream:
            header = Int8.from_stream(stream)
            self.assertEqual(header.raw_bytes, b"\x11")
            obj = ArraySingleString.from_stream(stream)

            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

    def test_get_object_id(self) -> int:
        pass

    def test_get_name(self):
        pass

    def test_get_string(self):
        pass

    def find_text(self):
        pass

    def test_replace_text(self):
        pass

    def get_all_texts(self):
        pass

if __name__ == '__main__':
    unittest.main()
