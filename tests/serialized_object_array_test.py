from typing import BinaryIO
import unittest

from core.primitives import LengthPrefixedString
from core.serialized_object_array import SerializedObjectArray, BinaryType

class SerializedObjectArrayTest(unittest.TestCase):

    def assertEndOfStream(self, stream: BinaryIO):
        self.assertEqual(stream.read(1), b"\x0b")
        self.assertEqual(stream.read(1), b"")

    def test_read_from_stream_string_array(self):
        """
        注: ユニットテスト的になぜこれが入るのか疑問に思うかもしれないが、
        underrailアーカイブの要素を頭から順に読み取る実装をしていると先にStringのみのArrayがでてくる、という都合から。
        :return:
        """
        type_list = [BinaryType.String] * 19
        with open("data/string_array", "rb") as stream:
            array = SerializedObjectArray.from_stream(stream, 19, type_list)
            self.assertEndOfStream(stream)

            stream.seek(0)
            expected_raw_bytes = stream.read()[:-1]

        EXPECTED_STRINGS = [ 'I:C', 'I:N', 'I:Q', 'I:L', 'I:D', 'I:VM', 'I:MS', 'I:C2', 'I:CV', 'I:CP',
                             'I:IVF', 'I:CS:Count', 'I:I', 'I:R', 'I:S', 'I:T', 'I:W', 'I:CR', 'NEI:CR' ]

        for i in range(19):
            obj = array.get_item(i)
            self.assertIsInstance(obj, LengthPrefixedString)
            self.assertEqual(obj.string, EXPECTED_STRINGS[i])
        self.assertEqual(array.raw_bytes, expected_raw_bytes)

if __name__ == '__main__':
    unittest.main()
