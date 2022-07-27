from io import BytesIO
import mock
import unittest

from underrail_translation_kit.msnrbf_parser.enums import RecordType, BinaryArrayType, BinaryType
from underrail_translation_kit.msnrbf_parser.primitives import RecordHeader
from underrail_translation_kit.msnrbf_parser.serialized_object import SerializedObject
from .helper import assertEndOfStream, assertEqualToStream
from underrail_translation_kit.msnrbf_parser.loaders import load_binary_array

class BinaryArrayLoaderTest(unittest.TestCase):

    @mock.patch("underrail_translation_kit.msnrbf_parser.loaders.load_class_with_id")
    @mock.patch("underrail_translation_kit.msnrbf_parser.structure.ClassTypeInfo.from_stream")
    def test_for_single_class_array(self, mock_lcwi, mock_CTIfs):
        mock_lcwi.return_value = SerializedObject(b"\x01")
        mock_CTIfs.return_value = SerializedObject(b"")

        input_bytes = RecordHeader(RecordType.BinaryArray).raw_bytes
        input_bytes += int(123456).to_bytes(4, "little")    # objectid
        input_bytes += BinaryArrayType.Single.value.to_bytes(1, "little")
        input_bytes += int(1).to_bytes(4, "little") # rank
        input_bytes += int(1).to_bytes(4, "little") # lengths
        input_bytes += BinaryType.Class.value.to_bytes(1, "little")

        # members
        input_bytes += RecordHeader(RecordType.ClassWithId).raw_bytes

        stream = BytesIO(input_bytes)
        stream.seek(1) # ヘッダを消費

        result = load_binary_array(stream, {})
        assertEndOfStream(self, stream)
        assertEqualToStream(self, result.raw_bytes, stream)


if __name__ == '__main__':
    unittest.main()
