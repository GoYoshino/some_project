from enum import Enum

class BinaryType(Enum):
    Primitive = 0
    String = 1
    Object = 2
    SystemClass = 3
    Class = 4
    ObjectArray = 5
    StringArray = 6
    PrimitiveArray = 7

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

class PrimitiveType(Enum):
    NonPrimitive = 999
    Boolean = 1
    Double = 6
    Int16 = 7
    Int32 = 8
    Single = 11