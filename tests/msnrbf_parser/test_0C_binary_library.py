import unittest

from underrail_translation_kit.msnrbf_parser.primitives import Int8
from underrail_translation_kit.msnrbf_parser.misc_record_classes import BinaryLibrary
from .helper import assertEndOfStream, assertEqualToStream

class BinaryLibraryTest(unittest.TestCase):

    def test_reading_stream(self):
        with open("msnrbf_parser/data/0C_BinaryLibrary", "rb") as stream:
            # The first byte has to externalized because actual parser should change behavior according to record type
            header = Int8.from_stream(stream)
            self.assertEqual(header.raw_bytes, b"\x0C")
            obj = BinaryLibrary.from_stream(stream)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

if __name__ == '__main__':
    unittest.main()
