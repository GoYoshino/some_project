import unittest

from underrail_translation_kit.msnrbf_parser.misc_record_classes import ClassWithID
from .helper import assertEndOfStream, assertEqualToStream

class ClassInfoTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("msnrbf_parser/data/01_ClassWithID", "rb") as stream:
            header = stream.read(1)
            self.assertEqual(header, b"\x01")
            obj = ClassWithID.from_stream(stream)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

            # Do not confirm detailed class behavior because we are not interested in as long as constructed binary is valid

if __name__ == '__main__':
    unittest.main()
