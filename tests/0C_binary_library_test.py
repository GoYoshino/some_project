import unittest

from core.primitives import Int8
from core.record import BinaryLibrary
from tests.helpers.bytes_asserts import assertEndOfStream, assertEqualToStream

class BinaryLibraryTest(unittest.TestCase):

    def test_reading_stream(self):
        with open("data/0C_BinaryLibrary", "rb") as stream:
            # The first byte has to externalized because actual parser should change behavior according to record type
            record_type = Int8.from_stream(stream)
            obj = BinaryLibrary.from_stream(stream, record_type)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

if __name__ == '__main__':
    unittest.main()
