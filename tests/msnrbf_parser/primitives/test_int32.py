from io import BytesIO
import unittest

from underrail_translation_kit.msnrbf_parser.primitives import Int32
from tests.msnrbf_parser.helper import assertEndOfStream

class Int32Test(unittest.TestCase):
    def test_reading_stream(self):
        raw_bytes = b"\x04\x02\x01\x02"
        stream = BytesIO(raw_bytes)

        obj = Int32.from_stream(stream)
        self.assertEqual(obj.value(), 33620484)
        assertEndOfStream(self, stream)
        self.assertEqual(obj.raw_bytes, raw_bytes)

if __name__ == '__main__':
    unittest.main()
