from typing import List

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
                dictionary[item.get_name()] = item

        return dictionary

    def has_member_class(self, name: str) -> bool:
        return name in self.__dictionary.keys()

    def get_member_class(self, name: str) -> ClassWithMembersAndTypes:
        return self.__dictionary[name]