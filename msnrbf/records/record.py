from enum import Enum
from typing import BinaryIO

from msnrbf.core.serialized_object import SerializedObject, LengthPrefixedString

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

# note that header(1byte) is not contained
byte_length_for_records = {
    RecordType.SerializedStreamHeader: 16
}

class Record(SerializedObject):
    """
    Represents an abstract record.
    It can be instantiated and used if the record is irrelevant to translation.
    """

    def __init__(self, raw_bytes: bytes, recordType: RecordType):
        super().__init__(raw_bytes)
        self.recordType = recordType

    def __repr__(self):
        return(f"type: {self.recordType}, bytes={self.rawBytes}")

class BinaryLibrary(Record):

    def __init__(self, libraryId: SerializedObject, libraryName: LengthPrefixedString):
        raw_bytes = b"\x0C" + libraryId.rawBytes + libraryName.rawBytes
        super().__init__(raw_bytes, RecordType.BinaryLibrary)
        self.libraryId = libraryId
        self.libraryName = libraryName

    def __repr__(self):
        return (f"type: {self.recordType}, libraryId: {str(self.libraryId)}, libraryName: {str(self.libraryName)}")