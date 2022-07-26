from io import BytesIO
from typing import BinaryIO

from .record import Record
from .primitives import LengthPrefixedString, Int8, Int32

class BinaryObjectString(Record):
    """
    Refers to 06: ClassWithMembersAndTypes Record
    *Does* care detailed behavior because it is relevant to translation work
    """

    def __init__(self, record_type: Int8, object_id: Int32, value: LengthPrefixedString):
        super().__init__(record_type, [object_id, value])
        self.__object_id = object_id
        self.__value = value

    def get_string(self) -> str:
        return self.__value.string

    def get_length(self) -> int:
        return self.__value.length

    def get_object_id(self) -> int:
        return self.__object_id.value()

    def replace_string(self, string: str) -> None:
        self.__value.replace_string(string)
        self.recalc_raw_bytes()

    @staticmethod
    def from_stream(stream: BinaryIO):
        """
            Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
            :param stream:
            :param record_type:
            :return:
        """
        record_type = Int8.from_stream(BytesIO(b"\x06"))
        object_id = Int32.from_stream(stream)
        value = LengthPrefixedString.from_stream(stream)
        return BinaryObjectString(record_type, object_id, value)

    def __repr__(self):
        return f"BinaryString(ID={str(self.__object_id)}): {str(self.__value)}"