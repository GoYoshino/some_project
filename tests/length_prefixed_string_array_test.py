import unittest

from core.primitives import LengthPrefixedString
from core.serialized_object_array import LengthPrefixedStringArray
from tests.helpers.bytes_asserts import assertEndOfStream, assertEqualToStream

class LengthPrefixedStringArrayTest(unittest.TestCase):

    def test_read_from_stream(self):
        with open("data/string_array", "rb") as stream:
            array = LengthPrefixedStringArray.from_stream(stream, 19)
            assertEndOfStream(self, stream)
            assertEqualToStream(self, array.raw_bytes, stream)

        EXPECTED_STRINGS = [ 'I:C', 'I:N', 'I:Q', 'I:L', 'I:D', 'I:VM', 'I:MS', 'I:C2', 'I:CV', 'I:CP',
                             'I:IVF', 'I:CS:Count', 'I:I', 'I:R', 'I:S', 'I:T', 'I:W', 'I:CR', 'NEI:CR' ]

        for i in range(19):
            obj = array.get_item(i)
            self.assertIsInstance(obj, LengthPrefixedString)
            self.assertEqual(obj.string, EXPECTED_STRINGS[i])

if __name__ == '__main__':
    unittest.main()
