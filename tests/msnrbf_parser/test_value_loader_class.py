from io import BytesIO
import mock
import unittest

from .helper import assertEndOfStream, assertEqualToStream
from underrail_translation_kit.msnrbf_parser.loaders import _load_class_value
from underrail_translation_kit.msnrbf_parser.serialized_object import SerializedObject

class ClassValueLoaderTest(unittest.TestCase):

    @mock.patch("underrail_translation_kit.msnrbf_parser.loaders.load_class_with_id")
    def test_loading_class_with_id(self, mocked):
        mocked.return_value = SerializedObject(b"\x01\x02\x03")

        stream = BytesIO(b"\x01")
        result = _load_class_value(stream, {})
        assertEndOfStream(self, stream)

        self.assertEqual(result.raw_bytes, b"\x01\x02\x03")
        assert mocked.called

    @mock.patch("underrail_translation_kit.msnrbf_parser.loaders.load_class_with_members_and_types")
    def test_loading_class_with_members_and_types(self, mocked):
        mocked.return_value = SerializedObject(b"\x01\x02\x03")

        stream = BytesIO(b"\x05")
        result = _load_class_value(stream, {})
        assertEndOfStream(self, stream)

        self.assertEqual(result.raw_bytes, b"\x01\x02\x03")
        assert mocked.called

    def test_loading_member_reference(self):
        # use actual value rather than a mock because available
        expected_idref = 2500
        stream = BytesIO(b"\x09" + expected_idref.to_bytes(4, "little"))

        result = _load_class_value(stream, {})
        assertEndOfStream(self, stream)

        # Does not care detailed behaviour
        assertEqualToStream(self, result.raw_bytes, stream)


if __name__ == '__main__':
    unittest.main()
