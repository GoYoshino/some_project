from enum import Enum
from typing import BinaryIO
import struct

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

class Int8(SerializedObject):

    def __init__(self, raw_bytes: bytes):
        super().__init__(raw_bytes)

    def value(self):
        return int.from_bytes(self.raw_bytes, "little")

    @staticmethod
    def from_stream(handle: BinaryIO):
        raw_bytes = handle.read(1)
        return Int8(raw_bytes)

    def __repr__(self):
        return f"int8({self.value()})"

class Int16(SerializedObject):

    def __init__(self, raw_bytes: bytes):
        super().__init__(self.raw_bytes)

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
    def from_stream(handle: BinaryIO):
        raw_bytes = handle.read(4)
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
    def from_stream(handle: BinaryIO):
        raw_bytes = handle.read(8)
        return Double(raw_bytes)

class KnickKnack(SerializedObject):
    """
    Who cares detailed internal of it as long as it preserves original raw bytes
    """

    def __init__(self, raw_bytes: bytes, size: int):
        super().__init__(raw_bytes)
        self.__size = size

    @staticmethod
    def from_stream(stream: BinaryIO, size: int):
        raw_bytes = stream.read(size)
        return KnickKnack(raw_bytes, size)

    def __repr__(self):
        return f"KnickKnack({self.__size})"

class LengthPrefixedString(SerializedObject):

    def __init__(self, raw_bytes: bytes, length: int, string: str):
        super().__init__(raw_bytes)
        self.length = length
        self.string = string

    def replace_string(self, string: str) -> None:
        string = lf_to_crlf(string)
        new_string_bytes = bytes(string, "utf-8")
        byte_length = len(new_string_bytes)

        prefix_bytes = divide_to_7bits(byte_length)

        self.raw_bytes = prefix_bytes + new_string_bytes
        self.string = string
        self.length = byte_length

    @staticmethod
    def from_stream(handle: BinaryIO):
        raw_length_bytes = b""
        length_byte_list = []
        for i in range(5):
            new_byte = handle.read(1)
            raw_length_bytes += new_byte
            length_byte_list.append(new_byte[0])

            if new_byte[0] & 0b10000000 == 0:
                break

        string_length = concat_7bits(length_byte_list)

        section_string = handle.read(string_length)
        string = section_string.decode("utf-8")

        raw_bytes = raw_length_bytes + section_string
        return LengthPrefixedString(raw_bytes, string_length, string)

    def __repr__(self):
        return f"{self.string}[{self.length}]"