from typing import BinaryIO, List

from core.primitives import Int8, Int32, LengthPrefixedString, NoneObject, PrimitiveType
from core.serialized_object import SerializedObject
from core.serialized_object_array import SerializedObjectArray, LengthPrefixedStringArray, BinaryTypeEnumArray, BinaryType

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

class ClassTypeInfo(SerializedObjectArray):

    def __init__(self, type_name: LengthPrefixedString, library_id: Int32):
        super().__init__([type_name, library_id])

    @staticmethod
    def from_stream(stream: BinaryIO):
        type_name = LengthPrefixedString.from_stream(stream)
        library_id = Int32.from_stream(stream)

        return ClassTypeInfo(type_name, library_id)

class AdditionalInfo(SerializedObjectArray):

    def __init__(self, items: List[SerializedObject]):
        super().__init__(items)

    @staticmethod
    def from_stream(stream: BinaryIO, binary_type_list: BinaryTypeEnumArray):
        count = binary_type_list.count()
        items = []

        for i in range(count):
            binary_type = binary_type_list.binary_type_at(i)
            if binary_type == BinaryType.Primitive:
                items.append(Int8.from_stream(stream))
            elif binary_type == BinaryType.Class:
                items.append(ClassTypeInfo.from_stream(stream))
            elif binary_type == BinaryType.String or binary_type == BinaryType.Object:
                items.append(NoneObject())
            else:
                raise Exception(f"Not implemented for {binary_type}")

        return AdditionalInfo(items)

class MemberTypeInfo(SerializedObjectArray):

    def __init__(self, binary_type_enums: BinaryTypeEnumArray, additional_info: AdditionalInfo):
        super().__init__([binary_type_enums, additional_info])

    @staticmethod
    def from_stream(stream: BinaryIO, count: int):
        binary_type_enums = BinaryTypeEnumArray.from_stream(stream, count)
        additional_info = AdditionalInfo.from_stream(stream, binary_type_enums)

        return MemberTypeInfo(binary_type_enums, additional_info)