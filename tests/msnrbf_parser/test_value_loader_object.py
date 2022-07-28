import unittest
from io import BytesIO

from underrail_translation_kit.msnrbf_parser.object_null import ObjectNull
from .helper import assertEndOfStream, assertEqualToStream
from underrail_translation_kit.msnrbf_parser.loaders import _load_object_value


class ObjectValueLoaderTest(unittest.TestCase):

    def test_loading_object_null(self):
        stream = BytesIO(b"\x0A")
        result = _load_object_value(stream)
        assertEndOfStream(self, stream)

        self.assertIsInstance(result, ObjectNull)
        assertEqualToStream(self, result.raw_bytes, stream)


if __name__ == '__main__':
    unittest.main()
