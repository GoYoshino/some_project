from io import BytesIO
import unittest

from underrail_translation_kit.msnrbf_parser.structure import ArrayInfo
from tests.msnrbf_parser.helper import assertEndOfStream

class Int32Test(unittest.TestCase):
    def test_reading_stream(self):
        raw_bytes = b"\x01\x00\x00\x00\x05\x00\x00\x00"
        stream = BytesIO(raw_bytes)

        obj = ArrayInfo.from_stream(stream)

        self.assertEqual(obj.get_length(), 5)

        assertEndOfStream(self, stream)
        self.assertEqual(obj.raw_bytes, raw_bytes)

if __name__ == '__main__':
    unittest.main()
