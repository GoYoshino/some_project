import unittest

from underrail_translation_kit.msnrbf_parser.structure import MemberTypeInfo
from tests.msnrbf_parser.helper import assertEndOfStream, assertEqualToStream

class MemberTypeInfoTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("msnrbf_parser/data/MemberTypeInfo", "rb") as stream:
            obj = MemberTypeInfo.from_stream(stream, 19)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

            # Do not confirm detailed class behavior because we are not interested in as long as constructed binary is valid

if __name__ == '__main__':
    unittest.main()
