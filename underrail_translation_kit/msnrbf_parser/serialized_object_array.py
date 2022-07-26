from typing import List, BinaryIO

from .enums import BinaryType
from .primitives import Int8, LengthPrefixedString
from .serialized_object import SerializedObject


class SerializedObjectArray(SerializedObject):

    def __init__(self, items: List[SerializedObject]):
        self.items = items
        raw_bytes = b""
        for item in items:
            raw_bytes += item.raw_bytes

        super().__init__(raw_bytes)

    def get_item(self, index: int) -> SerializedObject:
        assert index < len(self.items), f"index out of bounds: {index} for Array[{len(self.items)}]"
        return self.items[index]

    def __repr__(self):
        string = "["
        for item in self.items:
            string += str(item) + ","
        return string[:-1] + "]"

    def recalc_raw_bytes(self):
        raw_bytes = b""
        for item in self.items:
            item.recalc_raw_bytes()
            raw_bytes += item.raw_bytes
        self.raw_bytes = raw_bytes

class BinaryTypeEnumArray(SerializedObjectArray):

    def __init__(self, items: List[Int8]):
        super().__init__(items)

    def binary_type_at(self, index: int) -> BinaryType:
        return BinaryType(self.items[index].value())

    def count(self):
        return len(self.items)

    @staticmethod
    def from_stream(stream: BinaryIO, count: int):
        items = []
        for i in range(count):
            items.append(Int8.from_stream(stream))
        return BinaryTypeEnumArray(items)

    def __repr__(self):
        string = "["
        for i, item in enumerate(self.items):
            string += f"{self.binary_type_at(i).name}, "
        return string + "]"

class LengthPrefixedStringArray(SerializedObjectArray):

    def __init__(self, items: List[LengthPrefixedString]):
        super().__init__(items)

    def get_item(self, index) -> LengthPrefixedString:
        return self.items[index]

    @staticmethod
    def from_stream(stream: BinaryIO, count: int):
        items = []
        for i in range(count):
            items.append(LengthPrefixedString.from_stream(stream))

        return LengthPrefixedStringArray(items)