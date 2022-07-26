from io import BytesIO
import unittest

from underrail_translation_kit.msnrbf_parser.loaders import load_class_with_members_and_types, load_class_with_id
from .helper import assertEndOfStream, assertEqualToStream

class_info_source = b'\r\x00\x00\x00\x01P\x02\x00\x00\x00\x03P:N\x03P:V\x01\x00\x08\x02\x00\x00\x00\x06\x13\x00\x00\x00\rDamagePerTurn\x07\x00\x00\x00'

class ClassInfoTest(unittest.TestCase):

    def test_read_from_stream(self):
        class_info = load_class_with_members_and_types(BytesIO(class_info_source), {}).get_class_info_tuple()

        with open("msnrbf_parser/data/01_ClassWithID", "rb") as stream:
            header = stream.read(1)
            self.assertEqual(header, b"\x01")
            obj = load_class_with_id(stream, { 13: class_info })
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

            # Do not confirm detailed class behavior because we are not interested in as long as constructed binary is valid

if __name__ == '__main__':
    unittest.main()
