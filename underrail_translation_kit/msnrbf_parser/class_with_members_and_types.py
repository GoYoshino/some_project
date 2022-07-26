from .record import Record
from .structure import ClassInfo, MemberTypeInfo
from .primitives import Int8, Int32
from .value_array import ValueArray

class ClassWithMembersAndTypes(Record):
    """
    Refers to 05: ClassWithMembersAndTypes Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    """
    def __init__(self, record_type: Int8, class_info: ClassInfo, member_type_info: MemberTypeInfo, library_id: Int32, values: ValueArray):
        super().__init__(record_type, [class_info, member_type_info, library_id, values])

        self.__class_info = class_info
        self.__member_type_info = member_type_info
        self.__library_id = library_id
        self.__values = values

    def __repr__(self):
        return f"ClassWithMembersAndTypes: [{str(self.__class_info)}, {str(self.__member_type_info)}, {str(self.__library_id)}, values={str(self.__values)}]"