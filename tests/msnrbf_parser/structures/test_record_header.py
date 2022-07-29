from io import BytesIO
import unittest

from underrail_translation_kit.msnrbf_parser.primitives import RecordHeader
from underrail_translation_kit.msnrbf_parser.enums import RecordType

class RecordHeaderTest(unittest.TestCase):

    def test_parsing_enum(self):

        subject = RecordHeader(RecordType.ClassWithMembersAndTypes)

        self.assertEqual(subject.record_type, RecordType.ClassWithMembersAndTypes)
        self.assertEqual(subject.raw_bytes, b"\x05")

        stream = BytesIO(b"\x04")
        subject = RecordHeader.from_stream(stream)
        self.assertEqual(subject.record_type, RecordType.SystemClassWithMembersAndTypes)
        self.assertEqual(subject.raw_bytes, b"\04")

if __name__ == '__main__':
    unittest.main()
