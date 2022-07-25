from enum import Enum
from typing import List, BinaryIO

from core.primitives import Int8, LengthPrefixedString
from core.serialized_object import SerializedObject

class BinaryType(Enum):
    Primitive = 0
    String = 1
    Object = 2
    SystemClass = 3
    Class = 4
    ObjectArray = 5
    StringArray = 6
    PrimitiveArray = 7

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
        return string

class BinaryTypeEnumArray(SerializedObjectArray):

    def __init__(self, items: List[Int8]):
        super().__init__(items)

    def binary_type_at(self, index: int) -> BinaryType:
        return BinaryType(self.items[index].value())

    @staticmethod
    def from_stream(stream: BinaryIO, count: int):
        items = []
        for i in range(count):
            items.append(Int8.from_stream(stream))
        return BinaryTypeEnumArray(items)

class LengthPrefixedStringArray(SerializedObjectArray):

    def __init__(self, items: List[LengthPrefixedString]):
        super().__init__(items)

    @staticmethod
    def from_stream(stream: BinaryIO, count: int):
        items = []
        for i in range(count):
            items.append(LengthPrefixedString.from_stream(stream))

        return LengthPrefixedStringArray(items)