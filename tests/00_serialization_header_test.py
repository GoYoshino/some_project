import unittest

from core.primitives import Int8
from core.record import SerializationHeader
from tests.helpers.bytes_asserts import assertEndOfStream, assertEqualToStream

class SerializationHeaderTest(unittest.TestCase):

    def test_reading_stream(self):
        with open("data/00_SerializationHeader", "rb") as stream:
            # The first byte has to externalized because actual parser should change behavior according to record type
            header = Int8.from_stream(stream)
            self.assertEqual(header.raw_bytes, b"\x00")
            obj = SerializationHeader.from_stream(stream)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

if __name__ == '__main__':
    unittest.main()
