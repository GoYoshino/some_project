from enum import Enum
from typing import BinaryIO

from core.serialized_object import SerializedObject

class PrimitiveType(Enum):
    Boolean: 1
    Double: 6
    Int32: 8

class NoneObject(SerializedObject):
    """
    None, does not pose any
    """

    def __init__(self):
        super().__init__(b"")

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

    @staticmethod
    def from_stream(handle: BinaryIO):
        raw_bytes = handle.read(8)
        return Double(raw_bytes)

class LengthPrefixedString(SerializedObject):

    def __init__(self, raw_bytes: bytes, length: int, string: str):
        super().__init__(raw_bytes)
        self.length = length
        self.string = string

    @staticmethod
    def from_stream(handle: BinaryIO):
        section_string_length = handle.read(1)
        string_length = int.from_bytes(section_string_length, "little")

        section_string = handle.read(string_length)
        string = section_string.decode("utf-8")

        raw_bytes = section_string_length + section_string
        return LengthPrefixedString(raw_bytes, string_length, string)

    def __repr__(self):
        return f"{self.string}[{self.length}]"