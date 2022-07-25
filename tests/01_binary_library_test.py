import unittest
from typing import BinaryIO

from core.record import SerializationHeader

class SerializationHeaderTest(unittest.TestCase):

    def assertEndOfStream(self, stream: BinaryIO):
        self.assertEqual(stream.read(1), b"\x0b")
        self.assertEqual(stream.read(1), b"")

    def assertEqualToStream(self, raw_bytes: bytes, stream: BinaryIO):
        stream.seek(0)
        expected_raw_bytes = stream.read()[:-1]
        self.assertEqual(raw_bytes, expected_raw_bytes)

    def test_reading_stream(self):
        with open("data/00_SerializationHeader", "rb") as stream:
            obj = SerializationHeader.from_stream(stream)
            self.assertEndOfStream(stream)
            self.assertEqualToStream(obj.raw_bytes, stream)

if __name__ == '__main__':
    unittest.main()
