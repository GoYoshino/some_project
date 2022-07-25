import unittest

from core.primitives import LengthPrefixedString
from tests.helpers.bytes_asserts import assertEndOfStream

class LengthPrefixedStringTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("data/string", "rb") as stream:
            obj = LengthPrefixedString.from_stream(stream)
            assertEndOfStream(self, stream)
            stream.seek(0)
            expected_raw_bytes = stream.read()[:-1]

        self.assertEqual(obj.string, "This is the internal currency of the South Gate Station.")
        self.assertEqual(obj.length, 56)
        self.assertEqual(obj.raw_bytes, expected_raw_bytes)

    def test_works_on_loooong_text(self):
        with open("data/uirou_uri", "rb") as stream:
            obj = LengthPrefixedString.from_stream(stream)
            assertEndOfStream(self, stream)
            stream.seek(0)
            expected_raw_bytes = stream.read()[:-1]

        with open("data/uirou_uri.txt", "r", encoding="utf-8") as stream:
            self.assertEqual(obj.string, stream.read())
            self.assertEqual(obj.length, 2934)
            self.assertEqual(obj.raw_bytes, expected_raw_bytes)

if __name__ == '__main__':
    unittest.main()
