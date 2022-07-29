from typing import BinaryIO

from .enums import RecordType
from .record import Record
from .primitives import LengthPrefixedString, Int8, Int32, RecordHeader

class BinaryObjectString(Record):
    """
    Refers to 06: ClassWithMembersAndTypes Record
    *Does* care detailed behavior because it is relevant to translation work
    """

    def __init__(self, record_header: RecordHeader, object_id: Int32, value: LengthPrefixedString, meta_name: str=""):
        super().__init__(record_header, [object_id, value])
        self.__object_id = object_id
        self.__value = value
        self.meta_name = meta_name

    def get_string(self) -> str:
        return self.__value.string

    def get_length(self) -> int:
        return self.__value.string_byte_length

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
        record_type = RecordHeader(RecordType.BinaryObjectString)
        object_id = Int32.from_stream(stream)
        value = LengthPrefixedString.from_stream(stream)
        return BinaryObjectString(record_type, object_id, value)

    @staticmethod
    def from_params(object_id: int, string: str):
        record_type = RecordHeader(RecordType.BinaryObjectString)
        object_id = Int32.from_value(object_id)
        value = LengthPrefixedString.from_value(string)

    def __repr__(self):
        return f"BinaryString(ID={str(self.__object_id)}): {str(self.__value)}"