import unittest

from underrail_translation_kit.msnrbf_parser.loaders import load_binary_array
from underrail_translation_kit.msnrbf_parser.primitives import Int8
from .helper import assertEndOfStream, assertEqualToStream

class BinaryArrayTest(unittest.TestCase):

    def test_reading_stream(self):
        with open("msnrbf_parser/data/07_BinaryArray", "rb") as stream:
            # The first byte has to externalized because actual parser should change behavior according to record type
            header = Int8.from_stream(stream)
            self.assertEqual(header.raw_bytes, b"\x07")
            obj = load_binary_array(stream, {})
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

if __name__ == '__main__':
    unittest.main()
