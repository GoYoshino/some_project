from io import BytesIO
import unittest

from underrail_translation_kit.msnrbf_parser.primitives import Int8
from .helper import assertEndOfStream

class Int8Test(unittest.TestCase):

    def test_reading_stream(self):
        raw_bytes = b"\x12"
        stream = BytesIO(raw_bytes)

        obj = Int8.from_stream(stream)
        self.assertEqual(obj.value(), 18)
        assertEndOfStream(self, stream)
        self.assertEqual(obj.raw_bytes, raw_bytes),

if __name__ == '__main__':
    unittest.main()
