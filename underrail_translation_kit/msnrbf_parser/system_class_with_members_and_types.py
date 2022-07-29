from typing import Tuple

from .primitives import RecordHeader
from .record import Record
from .structure import ClassInfo, MemberTypeInfo
from .value_array import ValueArray

class SystemClassWithMembersAndTypes(Record):
    """
    Refers to 04: SystemClassWithMembersAndTypes Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    """
    def __init__(self, record_header: RecordHeader, class_info: ClassInfo, member_type_info: MemberTypeInfo, values: ValueArray):
        super().__init__(record_header, [class_info, member_type_info, values])

        self.__class_info = class_info
        self.__member_type_info = member_type_info
        self.__values = values

    def __repr__(self):
        return f"SystemClassWithMembersAndTypes: [{str(self.__class_info)}, {str(self.__member_type_info)}, values={str(self.__values)}]"

    def get_class_info_tuple(self) -> Tuple[ClassInfo, MemberTypeInfo]:
        return (self.__class_info, self.__member_type_info)