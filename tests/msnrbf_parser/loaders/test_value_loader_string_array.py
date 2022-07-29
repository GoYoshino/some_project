from io import BytesIO
import mock
import unittest

from underrail_translation_kit.msnrbf_parser.serialized_object import SerializedObject
from tests.msnrbf_parser.helper import assertEndOfStream, assertEqualToStream
from underrail_translation_kit.msnrbf_parser.loaders import _load_string_array_value
from underrail_translation_kit.msnrbf_parser.misc_record_classes import MemberReference


class StringValueLoaderTest(unittest.TestCase):

    @mock.patch("underrail_translation_kit.msnrbf_parser.misc_record_classes.ArraySingleString.from_stream")
    def test_loading_binary_object_string(self, mocked):
        mocked.return_value = SerializedObject(b"\x00\x22\x44")


        stream = BytesIO(b"\x11")
        result = _load_string_array_value(stream)
        assertEndOfStream(self, stream)

        self.assertEqual(result.raw_bytes, b"\x00\x22\x44")
        assert mocked.called


    def test_loading_member_reference(self):
        # use actual value rather than a mock because available
        expected_idref = 2500
        stream = BytesIO(b"\x09" + expected_idref.to_bytes(4, "little"))
        result = _load_string_array_value(stream)
        assertEndOfStream(self, stream)

        self.assertIsInstance(result, MemberReference)
        # Does not care detailed behaviour
        assertEqualToStream(self, result.raw_bytes, stream)

if __name__ == '__main__':
    unittest.main()
