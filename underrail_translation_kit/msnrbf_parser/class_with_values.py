import abc
from typing import List, Dict, Tuple

from underrail_translation_kit.msnrbf_parser.binary_object_string import BinaryObjectString
from underrail_translation_kit.msnrbf_parser.enums import BinaryType
from underrail_translation_kit.msnrbf_parser.misc_record_classes import MemberReference
from underrail_translation_kit.msnrbf_parser.primitives import RecordHeader
from underrail_translation_kit.msnrbf_parser.record import Record
from underrail_translation_kit.msnrbf_parser.record_with_values import RecordWithValues
from underrail_translation_kit.msnrbf_parser.serialized_object import SerializedObject
from underrail_translation_kit.msnrbf_parser.structure import ClassInfo, MemberTypeInfo
from underrail_translation_kit.msnrbf_parser.value_array import ValueArray



class ClassWithValues(Record, RecordWithValues):
    """
    valueのあるレコードの基底クラス。a.k.a.目的のブツを持っている奴
    BinaryObjectStringを持っている可能性があるため、共通の操作メソッドを持たせることにした。
    """

    def __init__(self, record_header: RecordHeader, meta_class_info: ClassInfo, meta_member_type_info: MemberTypeInfo, rest_items: List[SerializedObject], values: ValueArray):
        """

        :param record_header: レコードヘッダ
        :param meta_class_info: 必ずしもraw_bytesに*含まれない*事に注意
        :param meta_member_type_info: 必ずしもraw_bytesに*含まれない*事に注意
        :param rest_items: その他、raw_bytesに含めたいアイテムのリスト
        :param values: 値オブジェクトのリスト。raw_bytesに含まれる
        """
        super().__init__(record_header, rest_items + [values])
        self.__meta_class_info = meta_class_info
        self.__meta_member_type_info = meta_member_type_info
        self.__values = values

        self.__generate_member_dictionaries()

    def __generate_member_dictionaries(self) -> None:
        binary_type_list = self.__meta_member_type_info.get_binary_type_list()
        string_dictionary = {}
        record_with_value_dictionary = {}
        for i, binary_type in enumerate(binary_type_list):
            if binary_type == BinaryType.Class:
                item = self.__values.get_item(i)
                if not isinstance(item, RecordWithValues):
                    continue
                record_with_value_dictionary[item.get_object_id()] = item

            elif binary_type == BinaryType.String:
                item = self.__values.get_item(i)
                if isinstance(item, MemberReference):
                    continue
                assert isinstance(item, BinaryObjectString), f"not a BinaryObjectString: {item}"
                item_bos: BinaryObjectString = item
                string_dictionary[item_bos.get_object_id()] = item

        self.__string_member_dictionary = string_dictionary
        self.__record_with_value_dictionary = record_with_value_dictionary

    def get_name(self):
        return self.__meta_class_info.get_name()

    def has_string_member(self, object_id: int) -> bool:
        return object_id in self.__string_member_dictionary.keys()

    def get_string_member(self, object_id: int) -> BinaryObjectString:
        return self.__string_member_dictionary[object_id]

    def get_string_member_dict(self) -> Dict[int, BinaryObjectString]:
        return self.__string_member_dictionary

    def get_text(self, object_id: int) -> str:
        if self.has_string_member(object_id):
            return self.get_string_member(object_id).get_string()

        for member_record_with_value in self.__record_with_value_dictionary.values():
            if member_record_with_value.has_string_member(object_id):
                return member_record_with_value.get_text(object_id)

        raise Exception(f"{self} does not have member whose objectid='{object_id}'")

    def replace_text(self, new_string: str, object_id: int) -> None:
        if not self.has_string_member(object_id):
            raise Exception(f"{self} does not have member whose objectid='{object_id}'")
        self.get_string_member(object_id).replace_string(new_string)

    def get_class_info_tuple(self) -> Tuple[ClassInfo, MemberTypeInfo]:
        return (self.__meta_class_info, self.__meta_member_type_info)

    def get_all_texts(self, class_path: str="") -> Dict[int, BinaryObjectString]:
        class_path += "." + self.__meta_class_info.get_name()
        result = {}
        for i in range(self.__meta_class_info.count()):
            item = self.__values.get_item(i)
            if isinstance(item, RecordWithValues):
                result.update(item.get_all_texts(class_path))
            elif isinstance(item, BinaryObjectString):
                item.meta_name = class_path + "." + self.__meta_class_info.get_member_name_list()[i]
                result[item.get_object_id()] = item

        return result