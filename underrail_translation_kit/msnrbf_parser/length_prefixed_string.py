from enum import Enum
from io import BytesIO
from typing import BinaryIO, Tuple

from underrail_translation_kit.msnrbf_parser.serialized_object import SerializedObject
from .math_ import concat_7bits, divide_to_7bits
from .util import lf_to_crlf

def string_to_length_prefix_and_bytes(string: str) -> Tuple[bytes, bytes]:
    string_bytes = bytes(string, "utf-8")
    string_byte_length = len(string_bytes)
    prefix_bytes = divide_to_7bits(string_byte_length)

    return (prefix_bytes, string_bytes)


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