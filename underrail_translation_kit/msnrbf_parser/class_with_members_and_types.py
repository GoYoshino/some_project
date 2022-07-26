from typing import Dict, Tuple

from .binary_object_string import BinaryObjectString
from .enums import BinaryType
from .misc_record_classes import MemberReference
from .primitives import RecordHeader, Int32
from .record import Record
from .structure import ClassInfo, MemberTypeInfo
from .value_array import ValueArray

class ClassWithMembersAndTypes(Record):
    """
    Refers to 05: ClassWithMembersAndTypes Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    """
    def __init__(self, record_type: RecordHeader, class_info: ClassInfo, member_type_info: MemberTypeInfo, library_id: Int32, values: ValueArray):
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
        dictionary = {}
        for i, binary_type in enumerate(binary_type_list):
            if binary_type != BinaryType.String:
                continue
            item = self.__values.get_item(i)
            if isinstance(item, MemberReference):
                continue
            assert isinstance(item, BinaryObjectString), f"not a BinaryString: {item}"
            item_bos: BinaryObjectString = item
            dictionary[item_bos.get_object_id()] = item

        self.__string_member_dictionary = dictionary

    def get_object_id(self) -> int:
        return self.__class_info.get_object_id()

    def get_name(self) -> str:
        return self.__class_info.get_name()

    def has_string_member(self, object_id: int) -> bool:
        return object_id in self.__string_member_dictionary.keys()

    def get_string_member(self, object_id: int) -> BinaryObjectString:
        return self.__string_member_dictionary[object_id]

    def get_string_member_dict(self) -> Dict[int, BinaryObjectString]:
        return self.__string_member_dictionary

    def get_text(self, object_id: int) -> str:
        if not self.has_string_member(object_id):
            raise Exception(f"{self} does not have member whose objectid='{object_id}'")
        return self.get_string_member(object_id).get_string()

    def replace_text(self, new_string: str, object_id: int) -> None:
        if not self.has_string_member(object_id):
            raise Exception(f"{self} does not have member whose objectid='{object_id}'")
        self.get_string_member(object_id).replace_string(new_string)

    def get_class_info_tuple(self) -> Tuple[ClassInfo, MemberTypeInfo]:
        return (self.__class_info, self.__member_type_info)