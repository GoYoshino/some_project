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

    def replace_text(self, new_text: str, path: str) -> None:
        """
        Replaces certain text in certain path.
        Path contains class names separated by ".", like as typical member access.
        for example: to access BinaryString I:D in C00, the path will be "C00.I:D".
        path length is limited to 2, for now.
        :param new_string: new string
        :param path: path to the binarystring
        """
        paths = path.split(".")
        assert len(paths) == 2  # assuming there is no BinaryString directly under root node. may be changed later

        if (self.has_member_class(paths[0])):
            cls = self.get_member_class(paths[0])
            cls.replace_text(new_text, paths[1])

        self.recalc_raw_bytes()

    def has_member_class(self, name: str) -> bool:
        return name in self.__dictionary.keys()

    def get_member_class(self, name: str) -> ClassWithMembersAndTypes:
        return self.__dictionary[name]