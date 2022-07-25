import unittest

from core.primitives import Int8
from core.record import ClassWithMembersAndTypes
from tests.helpers.bytes_asserts import assertEndOfStream, assertEqualToStream

class ClassWithMembersTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("data/05_ClassWithMembersAndTypes", "rb") as stream:
            header = Int8.from_stream(stream)
            self.assertEqual(header.raw_bytes, b"\x05")
            obj = ClassWithMembersAndTypes.from_stream(stream)

            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

if __name__ == '__main__':
    unittest.main()
