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

if __name__ == '__main__':
    unittest.main()
