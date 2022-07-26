from typing import Dict, Tuple

from .binary_object_string import BinaryObjectString
from .enums import BinaryType
from .misc_record_classes import MemberReference
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
            assert isinstance(item, BinaryObjectString) or isinstance(item, MemberReference), f"not a BinaryString nor MemberReference: {item}"
            dictionary[member_name_list[i]] = item

        self.__string_member_dictionary = dictionary

    def has_string_member(self, member_name: str) -> bool:
        return member_name in self.__string_member_dictionary.keys()

    def get_string_member(self, member_name: str) -> BinaryObjectString:
        return self.__string_member_dictionary[member_name]

    def get_string_member_dict(self) -> Dict[str, BinaryObjectString]:
        return self.__string_member_dictionary

    def get_name(self) -> str:
        return self.__class_info.get_name()

    def get_text(self, member_name: str) -> str:
        if not self.has_string_member(member_name):
            raise Exception(f"{self} does not have member '{member_name}'")
        return self.get_string_member(member_name).get_string()

    def replace_text(self, new_string: str, member_name: str) -> None:
        if not self.has_string_member(member_name):
            raise Exception(f"{self} does not have member '{member_name}'")
        self.get_string_member(member_name).replace_string(new_string)

    def get_class_info_tuple(self) -> Tuple[ClassInfo, MemberTypeInfo]:
        return (self.__class_info, self.__member_type_info)