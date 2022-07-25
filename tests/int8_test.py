from io import BytesIO
from typing import BinaryIO
import unittest

from core.primitives import Int8

class Int8Test(unittest.TestCase):

    def assertEndOfStream(self, stream: BinaryIO):
        self.assertEqual(stream.read(1), b"\x0b")
        self.assertEqual(stream.read(1), b"")

    def test_reading_stream(self):
        raw_bytes = b"\x12"
        stream = BytesIO(raw_bytes + b"\x0b") #\x0bは停止確認のためのコード MS-NRBFに合わせてある

        obj = Int8.from_stream(stream)
        self.assertEqual(obj.value(), 18)
        self.assertEndOfStream(stream)
        self.assertEqual(obj.raw_bytes, raw_bytes),

if __name__ == '__main__':
    unittest.main()
