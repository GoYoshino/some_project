import unittest

from underrail_translation_kit.msnrbf_parser import parse_binary_stream
from .helper import assertEqualToStream

LOREM = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ac nisl lacus. Aenean sed facilisis augue. Aliquam erat volutpat. Aenean sit amet diam sed nisi porta faucibus ut nec eros. Sed sit amet tellus volutpat, consequat nisl ac, congue nunc. Nulla vel sapien nibh. Ut aliquet dolor eget commodo aliquet. Proin ipsum nulla, luctus in erat eget, facilisis fermentum felis. Praesent iaculis pulvinar sem vel tempor. Aenean lectus mi, varius id elit accumsan, ultricies maximus magna. Aliquam a tortor ante.\r\n\r\nVivamus nunc nisi, dignissim sit amet leo ut, viverra commodo tellus. Phasellus dapibus metus a sapien pretium, in faucibus neque sagittis. Curabitur et neque eu nulla egestas vestibulum. Nullam finibus, nisi scelerisque malesuada pretium, lacus orci pellentesque elit, sed congue orci eros sit amet metus. Proin id placerat tortor. Donec nec lacus sapien. Cras egestas, ante quis hendrerit lobortis, enim tellus luctus libero, eget ullamcorper elit dolor in arcu. Phasellus ac libero malesuada, scelerisque felis id, finibus quam. Aliquam erat volutpat. Quisque ultrices augue faucibus risus consequat facilisis. Donec ornare varius eleifend."

class RecalcTest(unittest.TestCase):

    def test_replace_and_recalc(self):
        print(b"\r")
        with open("msnrbf_parser/data/sgscredits", "rb") as f:
            result = parse_binary_stream(f)
            assertEqualToStream(self, result.raw_bytes, f)

        description = result.get_member_class("C00").get_string_member("I:D")
        description.replace_string(LOREM)
        self.assertEqual(description.get_length(), 1158)
        self.assertEqual(description.get_string(), LOREM)

        result.recalc_raw_bytes()

        with open("msnrbf_parser/data/sgscredits_changed", "rb") as f2:
            assertEqualToStream(self, result.raw_bytes, f2)

if __name__ == '__main__':
    unittest.main()
