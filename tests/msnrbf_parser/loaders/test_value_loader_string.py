import unittest
from io import BytesIO

from tests.msnrbf_parser.helper import assertEndOfStream, assertEqualToStream
from underrail_translation_kit.msnrbf_parser.binary_object_string import BinaryObjectString
from underrail_translation_kit.msnrbf_parser.loaders import _load_string_value
from underrail_translation_kit.msnrbf_parser.misc_record_classes import MemberReference

class StringValueLoaderTest(unittest.TestCase):

    def test_loading_binary_object_string(self):
        stream = BytesIO(b"\x06\x01\x00\x00\x00\x0BPatrolRoute")
        result = _load_string_value(stream)
        assertEndOfStream(self, stream)

        self.assertIsInstance(result, BinaryObjectString)
        self.assertEqual(result.get_object_id(), 1)
        self.assertEqual(result.get_string(), "PatrolRoute")
        assertEqualToStream(self, result.raw_bytes, stream)

    def test_loading_member_reference(self):
        # use actual value rather than a mock because available
        expected_idref = 2500
        stream = BytesIO(b"\x09" + expected_idref.to_bytes(4, "little"))
        result = _load_string_value(stream)
        assertEndOfStream(self, stream)

        self.assertIsInstance(result, MemberReference)
        # Does not care detailed behaviour
        assertEqualToStream(self, result.raw_bytes, stream)

if __name__ == '__main__':
    unittest.main()
