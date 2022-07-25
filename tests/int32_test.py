from io import BytesIO
from typing import BinaryIO
import unittest

from core.primitives import Int32

class Int32Test(unittest.TestCase):

    def assertEndOfStream(self, stream: BinaryIO):
        self.assertEqual(stream.read(1), b"\x0b")
        self.assertEqual(stream.read(1), b"")

    def test_reading_stream(self):
        raw_bytes = b"\x04\x02\x01\x02"
        stream = BytesIO(raw_bytes + b"\x0b") #\x0bは停止確認のためのコード MS-NRBFに合わせてある

        obj = Int32.from_stream(stream)
        self.assertEqual(obj.value(), 33620484)
        self.assertEqual(obj.raw_bytes, raw_bytes)
        self.assertEndOfStream(stream)

if __name__ == '__main__':
    unittest.main()
