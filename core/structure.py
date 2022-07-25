from enum import Enum
from typing import BinaryIO, List

from core.primitives import Int8, Int32, Double, LengthPrefixedString, NoneObject, PrimitiveType
from core.serialized_object import SerializedObject
from core.serialized_object_array import SerializedObjectArray, LengthPrefixedStringArray, BinaryTypeEnumArray, BinaryType
from core.binary_object_string import BinaryObjectString



class ClassInfo(SerializedObjectArray):

    def __init__(self, object_id: Int32, name: LengthPrefixedString, member_count: Int32, member_names: LengthPrefixedStringArray):
        self.__member_count_value = member_count.value()
        super().__init__([object_id, name, member_count, member_names])
        self.__object_id = object_id
        self.__name = name

    def count(self):
        return self.__member_count_value

    @staticmethod
    def from_stream(stream: BinaryIO):
        object_id = Int32.from_stream(stream)
        name = LengthPrefixedString.from_stream(stream)
        member_count = Int32.from_stream(stream)
        member_names = LengthPrefixedStringArray.from_stream(stream, member_count.value())

        return ClassInfo(object_id, name, member_count, member_names)

    def __repr__(self):
        return f"<ClassInfo: ObjectID={self.__object_id} name={self.__name} MembersCount={self.__member_count_value}>"

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
        self.__binary_type_enums = binary_type_enums
        self.__additional_info = additional_info

    @staticmethod
    def from_stream(stream: BinaryIO, count: int):
        binary_type_enums = BinaryTypeEnumArray.from_stream(stream, count)
        additional_info = AdditionalInfo.from_stream(stream, binary_type_enums)

        return MemberTypeInfo(binary_type_enums, additional_info)

    def get_binary_type_list(self):
        result = []
        for item in self.__binary_type_enums.items:
            result.append(BinaryType(item.value()))

        return result

    def get_primitive_enum_list(self):
        result = []
        for i, item in enumerate(self.__additional_info.items):
            if self.__binary_type_enums.binary_type_at(i) == BinaryType.Primitive:
                value = self.__additional_info.get_item(i).value()
                result.append(PrimitiveType(value))
            else:
                result.append(PrimitiveType.NonPrimitive)
        return result

    def __repr__(self):
        return f"[MemberTypeInfo BinaryTypeEnums={self.__binary_type_enums} AdditionalInfos={self.__additional_info}]"

class ObjectNull(SerializedObjectArray):
    """
    Refers to 0A: BinaryLibrary Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    Because header has nothing to do with translation work
    """

    def __init__(self, record_type: Int8):
        super().__init__([])
