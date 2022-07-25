from typing import BinaryIO

from core.primitives import Int32, LengthPrefixedString
from core.serialized_object_array import SerializedObjectArray, LengthPrefixedStringArray

class ClassInfo(SerializedObjectArray):

    def __init__(self, object_id: Int32, name: LengthPrefixedString, member_count: Int32, member_names: LengthPrefixedStringArray):
        super().__init__([object_id, name, member_count, member_names])

    @staticmethod
    def from_stream(stream: BinaryIO):
        object_id = Int32.from_stream(stream)
        name = LengthPrefixedString.from_stream(stream)
        member_count = Int32.from_stream(stream)
        member_names = LengthPrefixedStringArray.from_stream(stream, member_count.value())

        return ClassInfo(object_id, name, member_count, member_names)