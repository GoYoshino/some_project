import unittest

from underrail_translation_kit.msnrbf_parser.primitives import Int8
from underrail_translation_kit.msnrbf_parser.misc_record_classes import SerializationHeader
from tests.msnrbf_parser.helper import assertEndOfStream, assertEqualToStream

class SerializationHeaderTest(unittest.TestCase):

    def test_reading_stream(self):
        with open("msnrbf_parser/data/00_SerializationHeader", "rb") as stream:
            # The first byte has to externalized because actual parser should change behavior according to record type
            header = Int8.from_stream(stream)
            self.assertEqual(header.raw_bytes, b"\x00")
            obj = SerializationHeader.from_stream(stream)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

if __name__ == '__main__':
    unittest.main()
