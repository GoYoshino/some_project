import unittest

from underrail_translation_kit.msnrbf_parser.serialized_object_array import BinaryTypeEnumArray, BinaryType
from .helper import assertEndOfStream, assertEqualToStream

class BinaryTypeEnumArrayTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("msnrbf_parser/data/BinaryTypeEnumArray", "rb") as stream:
            array = BinaryTypeEnumArray.from_stream(stream, 19)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, array.raw_bytes, stream)

        EXPECTED_TYPES = [ BinaryType.String, BinaryType.String, BinaryType.Class, BinaryType.Primitive, BinaryType.String,
                           BinaryType.String, BinaryType.Primitive, BinaryType.Primitive, BinaryType.Primitive, BinaryType.Class,
                           BinaryType.Object, BinaryType.Primitive, BinaryType.Primitive, BinaryType.Class, BinaryType.Class,
                           BinaryType.Class, BinaryType.Primitive, BinaryType.Primitive, BinaryType.Primitive
                        ]

        for i in range(19):
            self.assertEqual(array.binary_type_at(i), EXPECTED_TYPES[i], f"index={i}")

if __name__ == '__main__':
    unittest.main()
