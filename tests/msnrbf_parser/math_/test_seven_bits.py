import unittest

from underrail_translation_kit.msnrbf_parser.math_ import concat_7bits, divide_to_7bits

class SevenBitsTest(unittest.TestCase):

    def test_concat_on_lower_than_128(self):
        byte_list = [ 69 ]
        result = concat_7bits(byte_list)
        self.assertEqual(byte_list[0], result)

        res = divide_to_7bits(2934)
        for r in res:
            print(hex(r))

    def test_concat_on_up_to_14bits(self):
        byte_list = [ 0xB0, 0x01 ]
        result = concat_7bits(byte_list)
        self.assertEqual(176, result)

    def test_concat_on_up_to_21bits(self):
        byte_list = [ 0xA5, 0x92, 0x37 ]
        result = concat_7bits(byte_list)
        self.assertEqual(903461, result)

    def test_divide_on_lower_than_128(self):
        number = 69
        result = divide_to_7bits(69)
        self.assertSequenceEqual(result, [ number ])

    def test_divide_on_up_to_14bits(self):
        number = 176
        expected_list = [ 0xB0, 0x01 ]
        result = divide_to_7bits(number)
        self.assertSequenceEqual(result, expected_list)

    def test_divide_on_up_to_21bits(self):
        number = 903461
        expected_list = [ 0xA5, 0x92, 0x37 ]
        result = divide_to_7bits(number)
        self.assertSequenceEqual(result, expected_list)

if __name__ == '__main__':
    unittest.main()
