"""
Loaderのありうるすべての場合をカバーしたい
"""

import unittest

from underrail_translation_kit.msnrbf_parser.structure import ArrayInfo
from .helper import assertEndOfStream
from underrail_translation_kit.msnrbf_parser.loaders import __load_string_value

class ValueLoaderTest(unittest.TestCase):
    def test_string_loader(self):


        raw_bytes = b"\x01\x00\x00\x00\x05\x00\x00\x00"
        stream = BytesIO(raw_bytes)

        obj = ArrayInfo.from_stream(stream)

        self.assertEqual(obj.get_length(), 5)

        assertEndOfStream(self, stream)
        self.assertEqual(obj.raw_bytes, raw_bytes)

if __name__ == '__main__':
    unittest.main()
