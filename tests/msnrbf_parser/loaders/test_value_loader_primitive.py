import unittest
from io import BytesIO

from underrail_translation_kit.msnrbf_parser.enums import PrimitiveType
from underrail_translation_kit.msnrbf_parser.primitives import KnickKnack, Int8, Int16, Int32, Double
from tests.msnrbf_parser.helper import assertEndOfStream, assertEqualToStream
from underrail_translation_kit.msnrbf_parser.loaders import _load_primitive_value


class PrimitiveValueLoaderTest(unittest.TestCase):

    def test_loading_boolean(self):
        stream = BytesIO(b"\x01")
        result = _load_primitive_value(stream, PrimitiveType.Boolean)
        assertEndOfStream(self, stream)

        self.assertIsInstance(result, KnickKnack)
        assertEqualToStream(self, result.raw_bytes, stream)

    def test_loading_int8(self):
        stream = BytesIO(b"\xFF")
        result = _load_primitive_value(stream, PrimitiveType.Byte)
        assertEndOfStream(self, stream)

        self.assertIsInstance(result, Int8)
        assertEqualToStream(self, result.raw_bytes, stream)

    def test_loading_int16(self):
        stream = BytesIO(b"\xFF\x01")
        result = _load_primitive_value(stream, PrimitiveType.Int16)
        assertEndOfStream(self, stream)

        self.assertIsInstance(result, Int16)
        assertEqualToStream(self, result.raw_bytes, stream)

    def test_loading_int32(self):
        stream = BytesIO(b"\xFF\x22\xAA\xBA")
        result = _load_primitive_value(stream, PrimitiveType.Int32)
        assertEndOfStream(self, stream)

        self.assertIsInstance(result, Int32)
        assertEqualToStream(self, result.raw_bytes, stream)

    def test_loading_int64(self):
        stream = BytesIO(b"\xFF\x22\xAA\xBA\xFF\x22\xAA\xBA")
        result = _load_primitive_value(stream, PrimitiveType.Int64)
        assertEndOfStream(self, stream)

        self.assertIsInstance(result, KnickKnack)
        assertEqualToStream(self, result.raw_bytes, stream)

    def test_loading_double(self):
        stream = BytesIO(b"\xFF\x22\xAA\xBA\xFF\x22\xAA\xBA")
        result = _load_primitive_value(stream, PrimitiveType.Double)
        assertEndOfStream(self, stream)

        self.assertIsInstance(result, Double)
        assertEqualToStream(self, result.raw_bytes, stream)

    def test_loading_single(self):
        stream = BytesIO(b"\xFF\x22\xAA\xBA")
        result = _load_primitive_value(stream, PrimitiveType.Single)
        assertEndOfStream(self, stream)

        self.assertIsInstance(result, KnickKnack)
        assertEqualToStream(self, result.raw_bytes, stream)

    def test_loading_uint32(self):
        stream = BytesIO(b"\xFF\x22\xAA\xBA")
        result = _load_primitive_value(stream, PrimitiveType.UInt32)
        assertEndOfStream(self, stream)

        self.assertIsInstance(result, KnickKnack)
        assertEqualToStream(self, result.raw_bytes, stream)

    def test_loading_timespan(self):
        stream = BytesIO(b"\xFF\x22\xAA\xBA\xFF\x22\xAA\xBA")
        result = _load_primitive_value(stream, PrimitiveType.TimeSpan)
        assertEndOfStream(self, stream)

        self.assertIsInstance(result, KnickKnack)
        assertEqualToStream(self, result.raw_bytes, stream)


if __name__ == '__main__':
    unittest.main()
