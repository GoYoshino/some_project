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


    def test_for_a_case_problematic(self):
        input = b"\x07\x1C\x00\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\x04\x03"
        input += b"\x65\x42\x54\x02\x00\x00\x00\x05\xE3\xFF\xFF\xFF\x03\x65\x42\x54"
        input += b"\x01\x00\x00\x00\x07\x76\x61\x6C\x75\x65\x5F\x5F\x00\x08\x02\x00"
        input += b"\x00\x00\x01\x00\x00\x00\x01\xE2\xFF\xFF\xFF\xE3\xFF\xFF\xFF\x04"
        input += b"\x00\x00\x00\x01\xE1\xFF\xFF\xFF\xE3\xFF\xFF\xFF\x05\x00\x00\x00"
        input += b"\x01\xE0\xFF\xFF\xFF\xE3\xFF\xFF\xFF\x00\x00\x00\x00"

        stream = BytesIO(input)
        stream.seek(1)
        result = load_binary_array(stream, {})
        assertEndOfStream(self, stream)
        assertEqualToStream(self, result.raw_bytes, stream)


if __name__ == '__main__':
    unittest.main()
