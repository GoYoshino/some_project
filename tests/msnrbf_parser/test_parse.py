import unittest

from underrail_translation_kit.msnrbf_parser import parse_binary_stream
from tests.msnrbf_parser.helper import assertEqualToStream

class ReadWholeFileTest(unittest.TestCase):

    def test_read_item_file(self):
        with open("msnrbf_parser/data/sgscredits", "rb") as f:
            result = parse_binary_stream(f)
            assertEqualToStream(self, result.raw_bytes, f)

            self.assertTrue(result.has_member_class("C00"))
            C00 = result.get_member_class("C00")
            self.assertTrue(C00.has_string_member("I:C"))
            self.assertEqual(C00.get_string_member("I:C").get_string(), "currency.sgs")
            self.assertTrue(C00.has_string_member("I:D"))
            self.assertEqual(C00.get_string_member("I:D").get_string(), "This is the internal currency of the South Gate Station.")

            self.assertEqual(result.get_text("C00.I:C"), "currency.sgs")
            self.assertEqual(result.get_text("C00.I:D"), "This is the internal currency of the South Gate Station.")

    def test_read_item_file2(self):
        with open("msnrbf_parser/data/stygiancoin", "rb") as f:
            result = parse_binary_stream(f)
            assertEqualToStream(self, result.raw_bytes, f)

    def test_read_knowledge_file(self):
        with open("msnrbf_parser/data/baseabilities", "rb") as f:
            result = parse_binary_stream(f)
            assertEqualToStream(self, result.raw_bytes, f)

if __name__ == '__main__':
    unittest.main()
