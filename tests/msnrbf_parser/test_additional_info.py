import unittest

from underrail_translation_kit.msnrbf_parser.structure import ClassInfo, AdditionalInfo
from underrail_translation_kit.msnrbf_parser.serialized_object_array import BinaryTypeEnumArray
from .helper import assertEndOfStream, assertEqualToStream

class ClassInfoTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("msnrbf_parser/data/BinaryTypeEnumArray", "rb") as stream:
            binary_types = BinaryTypeEnumArray.from_stream(stream, 19)

        with open("msnrbf_parser/data/AdditionalInfo", "rb") as stream:
            obj = AdditionalInfo.from_stream(stream, binary_types)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

            # Do not confirm detailed class behavior because we are not interested in as long as constructed binary is valid

if __name__ == '__main__':
    unittest.main()
