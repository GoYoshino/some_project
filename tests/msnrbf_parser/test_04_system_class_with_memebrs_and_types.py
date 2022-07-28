from io import BytesIO
import unittest

from underrail_translation_kit.msnrbf_parser.enums import RecordType
from underrail_translation_kit.msnrbf_parser.loaders import load_system_class_with_members_and_types
from underrail_translation_kit.msnrbf_parser.primitives import RecordHeader

from .helper import assertEndOfStream, assertEqualToStream

class SystemClassWithMembersTest(unittest.TestCase):

    def test_read_from_stream(self):
        stream = BytesIO(b'\x04=\x05\x00\x00\x0eSystem.Version\x04\x00\x00\x00\x06_Major\x06_Minor\x06_Build\t_Revision\x00\x00\x00\x00\x08\x08\x08\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        header = RecordHeader.from_stream(stream)
        self.assertEqual(header.record_type, RecordType.SystemClassWithMembersAndTypes)

        obj = load_system_class_with_members_and_types(stream, {})

        assertEndOfStream(self, stream)
        assertEqualToStream(self, obj.raw_bytes, stream)

if __name__ == '__main__':
    unittest.main()
