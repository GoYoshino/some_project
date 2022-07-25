import unittest

from core.structure import ClassTypeInfo
from tests.helpers.bytes_asserts import assertEndOfStream, assertEqualToStream

class ClassTypeInfoTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("data/ClassTypeInfo", "rb") as stream:
            pass
            obj = ClassTypeInfo.from_stream(stream)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

            # Do not confirm detailed class behavior because we are not interested in as long as constructed binary is valid

if __name__ == '__main__':
    unittest.main()
