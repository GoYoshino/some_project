import unittest

from core.primitives import Int8
from core.record import ClassWithId
from tests.helpers.bytes_asserts import assertEndOfStream, assertEqualToStream

class ClassWithIdTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("data/01_ClassWithId", "rb") as stream:
            header = Int8.from_stream(stream)
            self.assertEqual(header.raw_bytes, b"\x01")
            obj = ClassWithId.from_stream(stream)

            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

if __name__ == '__main__':
    unittest.main()
