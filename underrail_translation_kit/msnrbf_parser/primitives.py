from enum import Enum
from io import BytesIO
from typing import BinaryIO, Tuple
import struct

from .enums import RecordType
from .math_ import concat_7bits, divide_to_7bits
from .serialized_object import SerializedObject
from .util import lf_to_crlf

class NoneObject(SerializedObject):
    """
    None, does not pose any
    """

    def __init__(self):
        super().__init__(b"")

    def __repr__(self):
        return "(None)"

class RecordHeader(SerializedObject):

    def __init__(self, record_type: RecordType):
        raw_bytes = record_type.value.to_bytes(1, "little")
        self.record_type = record_type
        super().__init__(raw_bytes)

    @staticmethod
    def from_stream(stream: BinaryIO):
        result = stream.read(1)
        record_type = int.from_bytes(result, "little")
        return RecordHeader(RecordType(record_type))

    def __repr__(self):
        return f"Header:{self.record_type.name}({hex(self.record_type.value)})"


class Int8(SerializedObject):

    def __init__(self, raw_bytes: bytes):
        super().__init__(raw_bytes)

    def value(self):
        return int.from_bytes(self.raw_bytes, "little")

    @staticmethod
    def from_value(value: int):
        raw_bytes = value.to_bytes(1, "little")
        return Int32(raw_bytes)

    @staticmethod
    def from_stream(stream: BinaryIO):
        raw_bytes = stream.read(1)
        return Int8(raw_bytes)

    def __repr__(self):
        return f"int8({self.value()})"


class Int16(SerializedObject):

    def __init__(self, raw_bytes: bytes):
        super().__init__(raw_bytes)

    def value(self):
        return int.from_bytes(self.raw_bytes, "little")

    @staticmethod
    def from_stream(stream: BinaryIO):
        raw_bytes = stream.read(2)
        return Int16(raw_bytes)

    def __repr__(self):
        return f"int16({self.value()})"


class Int32(SerializedObject):

    def __init__(self, raw_bytes: bytes):
        super().__init__(raw_bytes)

    def value(self):
        return int.from_bytes(self.raw_bytes, "little")

    @staticmethod
    def from_value(value: int):
        raw_bytes = value.to_bytes(4, "little")
        return Int32(raw_bytes)

    @staticmethod
    def from_stream(stream: BinaryIO):
        raw_bytes = stream.read(4)
        return Int32(raw_bytes)

    def __repr__(self):
        return f"int32({self.value()})"


class Double(SerializedObject):

    def __init__(self, raw_bytes: bytes):
        super(). __init__(raw_bytes)

    # I will not implement value() method for this because it is not related to translation work
    # (possibly enables modding?)

    def value(self) -> float:
        return struct.unpack('<f', self.raw_bytes)[0]

    @staticmethod
    def from_stream(stream: BinaryIO):
        raw_bytes = stream.read(8)
        return Double(raw_bytes)


class KnickKnack(SerializedObject):
    """
    Who cares detailed internal of it as long as it preserves original raw bytes
    """

    def __init__(self, raw_bytes: bytes, size: int, name: str="knicknack"):
        super().__init__(raw_bytes)
        self.__size = size
        self.__name = name

    @staticmethod
    def from_stream(stream: BinaryIO, size: int, name: str="knicknack"):
        raw_bytes = stream.read(size)
        return KnickKnack(raw_bytes, size, name)

    def __repr__(self):
        return f"{self.__name}({self.raw_bytes})"


def string_to_length_prefix_and_bytes(string: str) -> Tuple[bytes, bytes]:
    string_bytes = bytes(string, "utf-8")
    string_byte_length = len(string_bytes)
    prefix_bytes = divide_to_7bits(string_byte_length)

    return (prefix_bytes, string_bytes)


# TODO: is this really "primitive"?
class LengthPrefixedString(SerializedObject):

    def __init__(self, raw_bytes: bytes, byte_length: int, string: str):
        super().__init__(raw_bytes)
        self.string_byte_length = byte_length
        self.string = string

    def replace_string(self, string: str) -> None:
        string = lf_to_crlf(string)
        prefix_bytes, string_bytes = string_to_length_prefix_and_bytes(string)
        self.raw_bytes = prefix_bytes + string_bytes
        self.string_byte_length = len(string_bytes)
        self.string = string

    @staticmethod
    def from_stream(stream: BinaryIO):
        raw_length_bytes = b""
        length_byte_list = []
        for i in range(5):
            new_byte = stream.read(1)
            raw_length_bytes += new_byte
            length_byte_list.append(new_byte[0])

            if new_byte[0] & 0b10000000 == 0:
                break

        string_byte_length = concat_7bits(length_byte_list)

        section_string = stream.read(string_byte_length)
        string = section_string.decode("utf-8")

        raw_bytes = raw_length_bytes + section_string
        return LengthPrefixedString(raw_bytes, string_byte_length, string)

    @staticmethod
    def from_value(string: str):
        prefix, string_bytes = string_to_length_prefix_and_bytes(string)
        return LengthPrefixedString(prefix + string_bytes, len(string_bytes), string)

    def __repr__(self):
        return f"{self.string}[{self.string_byte_length}]"