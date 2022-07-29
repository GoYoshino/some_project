from typing import BinaryIO
import struct

from .enums import RecordType
from .serialized_object import SerializedObject


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