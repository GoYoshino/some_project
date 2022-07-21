from typing import BinaryIO

class SerializedObject:
    def __init__(self, raw_bytes: bytes):
        self.rawBytes = raw_bytes

class Int8(SerializedObject):

    def __init__(self, rawBytes: bytes):
        super().__init__(rawBytes)

    def value(self):
        return int.from_bytes(self.rawBytes, "little")

    @staticmethod
    def fromStream(handle: BinaryIO):
        raw_bytes = handle.read(1)
        return Int8(raw_bytes)

    def __repr__(self):
        return f"int8({self.value()})"

class Int32(SerializedObject):

    def __init__(self, raw_bytes: bytes):
        super().__init__(raw_bytes)

    def value(self):
        return int.from_bytes(self.rawBytes, "little")

    @staticmethod
    def fromStream(handle: BinaryIO):
        rawBytes = handle.read(4)
        return Int8(rawBytes)

    def __repr__(self):
        return f"int32({self.value()})"

class LengthPrefixedString(SerializedObject):

    def __init__(self, raw_bytes: bytes, length: int, string: str):
        super().__init__(raw_bytes)
        self.length = length
        self.string = string

    @staticmethod
    def fromStream(handle: BinaryIO):
        section_string_length = handle.read(1)
        string_length = int.from_bytes(section_string_length, "little")

        section_string = handle.read(string_length)
        string = section_string.decode("utf-8")

        raw_bytes = section_string_length + section_string
        return LengthPrefixedString(raw_bytes, string_length, string)

    def __repr__(self):
        return f"{self.string}[{self.length}]"