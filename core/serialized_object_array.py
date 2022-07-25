from enum import Enum
from typing import List, BinaryIO

from core.serialized_object import SerializedObject
from core.primitives import LengthPrefixedString

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
        self.__items = items
        raw_bytes = b""
        for item in items:
            raw_bytes += item.raw_bytes

        super().__init__(raw_bytes)

    def get_item(self, index: int) -> SerializedObject:
        assert index < len(self.__items), f"index out of bounds: {index} for Array[{len(self.__items)}]"
        return self.__items[index]

    def __repr__(self):
        string = "["
        for item in self.__items:
            string += str(item) + ","
        return string