from typing import List, Dict

from .serialized_object import SerializedObject
from .serialized_object_array import SerializedObjectArray
from .class_with_members_and_types import ClassWithMembersAndTypes

class ParseResult(SerializedObjectArray):
    """
    A Serialzied Object container that provides simple member access
    """

    def __init__(self, items: List[SerializedObject]):
        super().__init__(items)
        self.__dictionary = self.__generate_dictionary()

    def __generate_dictionary(self):
        dictionary = {}
        for item in self.items:
            if isinstance(item, ClassWithMembersAndTypes):
                dictionary[item.get_object_id()] = item

        return dictionary

    def __find_target_class(self, object_id: int) -> ClassWithMembersAndTypes:
        target_class = None
        classes = self.get_member_class_dict()
        for key in classes:
            class_ = classes[key]
            if class_.has_string_member(object_id):
                return class_

        raise Exception(f"could not find a class with id={object_id}")

    def get_text(self, object_id: int) -> str:
        target_class = self.__find_target_class(object_id)
        return target_class.get_text(object_id)

    def replace_text(self, new_text: str, object_id: int) -> None:
        """
        Replaces certain text of certain object id.
        :param new_string: new string
        :param object_id: object ID
        """

        target_class = self.__find_target_class(object_id)
        target_class.replace_text(new_text, object_id)

        self.recalc_raw_bytes()

    def get_member_class_dict(self) -> Dict[int, ClassWithMembersAndTypes]:
        return self.__dictionary