from .binary_object_string import BinaryObjectString
from .enums import BinaryType
from .primitives import Int8, Int32
from .record import Record
from .structure import ClassInfo, MemberTypeInfo
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

        self.__generate_dictionary()

    def __repr__(self):
        return f"ClassWithMembersAndTypes: [{str(self.__class_info)}, {str(self.__member_type_info)}, {str(self.__library_id)}, values={str(self.__values)}]"

    def __generate_dictionary(self):
        binary_type_list = self.__member_type_info.get_binary_type_list()
        member_name_list = self.__class_info.get_member_name_list()
        dictionary = {}
        for i, binary_type in enumerate(binary_type_list):
            if binary_type != BinaryType.String:
                continue
            item = self.__values.get_item(i)
            assert isinstance(item, BinaryObjectString)
            dictionary[member_name_list[i]] = item

        self.__string_member_dictionary = dictionary

    def get_string_member(self, member_name: str) -> BinaryObjectString:
        if member_name not in self.__string_member_dictionary.keys():
            raise Exception(f"member '{member_name}' not found")
        else:
            return self.__string_member_dictionary[member_name]

    def get_name(self) -> str:
        return self.__class_info.get_name()