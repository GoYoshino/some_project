import unittest

from underrail_translation_kit.msnrbf_parser.loaders import load_class_with_members_and_types
from underrail_translation_kit.msnrbf_parser.primitives import RecordType, RecordHeader

from .helper import assertEndOfStream, assertEqualToStream

class ClassWithMembersTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("msnrbf_parser/data/05_ClassWithMembersAndTypes", "rb") as stream:
            header = RecordHeader.from_stream(stream)
            self.assertEqual(header.record_type, RecordType.ClassWithMembersAndTypes)
            obj = load_class_with_members_and_types(stream, {})

            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

if __name__ == '__main__':
    unittest.main()
