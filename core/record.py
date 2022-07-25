from enum import Enum
from io import BytesIO
from typing import BinaryIO, List

from core.primitives import Int8, Int32, Double, LengthPrefixedString
from core.serialized_object import SerializedObject
from core.serialized_object_array import SerializedObjectArray
from core.structure import ClassInfo, MemberTypeInfo, ValueType, ClassTypeInfo

class RecordType(Enum):
    SerializedStreamHeader = 0
    ClassWithId = 1
    SystemClassWithMembers = 2
    ClassWithMembers = 3
    SystemClassWithMembersAndTypes = 4
    ClassWithMembersAndTypes = 5
    BinaryObjectString = 6
    BinaryArray = 7
    MemberPrimitiveTyped = 8
    MemberReference = 9
    ObjectNull = 10
    MessageEnd = 11
    BinaryLibrary = 12
    ObjectNullMultiple256 = 13
    ObjectNullMultiple = 14
    ArraySinglePrimitive = 15
    ArraySingleObject = 16
    ArraySingleString = 17
    # 18 (Not defined in standard)
    # 19 (Not defined in standard)
    # 20 (Not defined in standard)
    MethodCall = 21
    MethodReturn = 22

    @classmethod
    def has_value(cls, value: int):
        return value in cls._value2member_map_

class Record(SerializedObjectArray):

    def __init__(self, record_type: Int8, items: List[SerializedObject]):
        assert RecordType.has_value(record_type.value())

        self.record_type = RecordType(record_type.value())

        super().__init__([record_type] + items)

class SerializationHeader(Record):
    """
    Refers to 00: SerializationHeader Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    Because header has nothing to do with translation work
    """

    def __init__(self, record_type: Int8, root_id: Int32, header_id: Int32, major_version: Int32, minor_version: Int32):
        super().__init__(record_type, [root_id, header_id, major_version, minor_version])

    @staticmethod
    def from_stream(stream: BinaryIO):
        """
        Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
        :param stream:
        :return:
        """
        record_type = Int8.from_stream(BytesIO(b"\x00"))
        root_id = Int32.from_stream(stream)
        header_id = Int32.from_stream(stream)
        major_version = Int32.from_stream(stream)
        minor_version = Int32.from_stream(stream)
        return SerializationHeader(record_type, root_id, header_id, major_version, minor_version)

class ClassWithMembersAndTypes(Record):
    """
    Refers to 05: ClassWithMembersAndTypes Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    """
    def __init__(self, record_type: Int8, class_info: ClassInfo, member_type_info: MemberTypeInfo, library_id: Int32):
        super().__init__(record_type, [class_info, member_type_info, library_id])

    @staticmethod
    def from_stream(stream: BinaryIO):
        """
            Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
            :param stream:
            :return:
        """
        record_type = Int8.from_stream(BytesIO(b"\x05"))
        class_info = ClassInfo.from_stream(stream)
        member_type_info = MemberTypeInfo.from_stream(stream, class_info.count())
        library_id = Int32.from_stream(stream)

        return ClassWithMembersAndTypes(record_type, class_info, member_type_info, library_id)

class BinaryObjectString(Record):
    """
    Refers to 06: ClassWithMembersAndTypes Record
    *Does* care detailed behavior because it is relevant to translation work
    """

    def __init__(self, record_type: Int8, object_id: Int32, value: LengthPrefixedString):
        super().__init__(record_type, [object_id, value])
        self.__value = value

    def get_string(self) -> str:
        return self.__value.raw_bytes[1:].decode("utf-8")

    def get_length(self) -> int:
        return self.__value.raw_bytes[0]

    @staticmethod
    def from_stream(stream: BinaryIO):
        """
            Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
            :param stream:
            :param record_type:
            :return:
        """
        record_type = Int8.from_stream(BytesIO(b"\x06"))
        object_id = Int32.from_stream(stream)
        value = LengthPrefixedString.from_stream(stream)
        return BinaryObjectString(record_type, object_id, value)

class MessageEnd(Record):
    """
    Refers to 0B: MessageEnd Record
    """

    def __init__(self):
        record_type = Int8.from_stream(BytesIO(b"\x0B"))
        super().__init__(record_type, [])


class BinaryLibrary(Record):
    """
    Refers to 0C: BinaryLibrary Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    Because header has nothing to do with translation work
    """

    def __init__(self, record_type: Int8, library_id: Int32, library_name: LengthPrefixedString):
        super().__init__(record_type, [library_id, library_name])

    @staticmethod
    def from_stream(stream: BinaryIO):
        """
            Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
            :param stream:
            :param record_type:
            :return:
        """
        record_type = Int8.from_stream(BytesIO(b"\x0C"))
        library_id = Int32.from_stream(stream)
        library_name = LengthPrefixedString.from_stream(stream)
        return BinaryLibrary(record_type, library_id, library_name)