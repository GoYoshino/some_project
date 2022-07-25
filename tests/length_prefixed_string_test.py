from typing import BinaryIO
import unittest

from core.primitives import LengthPrefixedString

class LengthPrefixedStringTest(unittest.TestCase):

    def assertEndOfStream(self, stream: BinaryIO):
        self.assertEqual(stream.read(1), b"\x0b")
        self.assertEqual(stream.read(1), b"")

    def test_read_from_stream(self):
        with open("data/string", "rb") as stream:
            obj = LengthPrefixedString.from_stream(stream)
            self.assertEndOfStream(stream)
            stream.seek(0)
            expected_raw_bytes = stream.read()[:-1]

        self.assertEqual(obj.string, "This is the internal currency of the South Gate Station.")
        self.assertEqual(obj.length, 56)
        self.assertEqual(obj.raw_bytes, expected_raw_bytes)

if __name__ == '__main__':
    unittest.main()
