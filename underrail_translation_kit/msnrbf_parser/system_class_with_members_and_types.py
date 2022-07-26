from .class_with_members_and_types import ClassWithMembersAndTypes
from .primitives import NoneObject
from .primitives import Int8, Int32
from .structure import ClassInfo, MemberTypeInfo
from .value_array import ValueArray

# TODO: implement common base class for Classes
class SystemClassWithMembersAndTypes(ClassWithMembersAndTypes):
    """
    Refers to 04: ClassWithMembersAndTypes Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    """
    def __init__(self, record_type: Int8, class_info: ClassInfo, member_type_info: MemberTypeInfo, values: ValueArray):
        self.__class_info = class_info
        self.__member_type_info = member_type_info
        self.__values = values
        # NoneObject has no side effect for now, but changed later
        super().__init__(record_type, class_info, member_type_info, NoneObject() ,values)

    def __repr__(self):
        return f"SystemClassWithMembersAndTypes: [{str(self.__class_info)}, {str(self.__member_type_info)}, values={str(self.__values)}]"