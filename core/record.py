from enum import Enum
from typing import List

from core.primitives import Int8
from core.serialized_object import SerializedObject
from core.serialized_object_array import SerializedObjectArray

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