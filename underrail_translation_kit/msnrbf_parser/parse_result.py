from typing import List, Dict

from underrail_translation_kit.msnrbf_parser.binary_object_string import BinaryObjectString
from underrail_translation_kit.msnrbf_parser.record_with_values import RecordWithValues
from .serialized_object import SerializedObject
from .serialized_object_array import SerializedObjectArray

class ParseResult(SerializedObjectArray):
    """
    A Serialzied Object container that provides simple member access
    """

    def __init__(self, items: List[SerializedObject]):
        super().__init__(items)
        self.__records_with_values_dict = self.__generate_record_with_values_dictionary()

    def __generate_record_with_values_dictionary(self) -> Dict[int, RecordWithValues]:
        dictionary = {}
        for item in self.items:
            if isinstance(item, RecordWithValues):
                assert item.get_object_id() not in dictionary
                dictionary[item.get_object_id()] = item
        return dictionary

    def __find_target_record(self, object_id: int) -> RecordWithValues:
        target_class = None
        classes = self.get_member_class_dict()
        for key in classes:
            class_ = classes[key]
            if class_.has_string(object_id):
                return class_

        raise Exception(f"could not find a class with id={object_id}")

    def get_text(self, object_id: int) -> str:
        target_class = self.__find_target_record(object_id)
        return target_class.get_text(object_id)

    def replace_text(self, new_text: str, object_id: int) -> None:
        """
        Replaces certain text of certain object id.
        :param new_string: new string
        :param object_id: object ID
        """

        target_class = self.__find_target_record(object_id)
        target_class.replace_text(new_text, object_id)

        self.recalc_raw_bytes()

    def get_member_class_dict(self) -> Dict[int, RecordWithValues]:
        return self.__records_with_values_dict

    def get_all_texts(self) -> Dict[int, BinaryObjectString]:
        result = {}
        for i, item in enumerate(self.items):
            if isinstance(item, RecordWithValues):
                result.update(item.get_all_texts(""))
            elif isinstance(item, BinaryObjectString):
                result[item.get_object_id()] = item

        return result