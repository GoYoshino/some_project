import abc
from typing import Dict

from underrail_translation_kit.msnrbf_parser.binary_object_string import BinaryObjectString


class RecordWithValues(metaclass=abc.ABCMeta):

    def get_object_id(self) -> int:
        raise NotImplementedError()

    def get_name(self) -> str:
        raise NotImplementedError()


    def has_string_member(self, object_id: int) -> bool:
        raise NotImplementedError()


    def get_string_member(self, object_id: int) -> BinaryObjectString:
        raise NotImplementedError()


    def get_string_member_dict(self) -> Dict[int, BinaryObjectString]:
        raise NotImplementedError()


    def get_text(self, object_id: int) -> str:
        raise NotImplementedError()


    def replace_text(self, new_string: str, object_id: int) -> None:
        raise NotImplementedError()

    def get_all_texts(self) -> Dict[int, BinaryObjectString]:
        raise NotImplementedError()