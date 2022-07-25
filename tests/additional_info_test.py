import unittest

from core.structure import ClassInfo, AdditionalInfo
from core.serialized_object_array import BinaryTypeEnumArray
from tests.helpers.bytes_asserts import assertEndOfStream, assertEqualToStream

class ClassInfoTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("data/BinaryTypeEnumArray", "rb") as stream:
            binary_types = BinaryTypeEnumArray.from_stream(stream, 19)

        with open("data/AdditionalInfo", "rb") as stream:
            obj = AdditionalInfo.from_stream(stream, binary_types)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

            # Do not confirm detailed class behavior because we are not interested in as long as constructed binary is valid

if __name__ == '__main__':
    unittest.main()
