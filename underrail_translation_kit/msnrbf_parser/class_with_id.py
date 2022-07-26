from typing import Dict, Tuple, BinaryIO
from io import BytesIO

from .loaders import load_values
from .primitives import Int8, Int32
from .record import Record
from .serialized_object_array import SerializedObjectArray
from .structure import ClassInfo, MemberTypeInfo


class ClassWithID(Record):
    """
        Refers to 01: ClassWithID Record
        Does not care detailed behavior as long as the instance preserves original raw byte array
        Because header has nothing to do with translation work
        """

    def __init__(self, record_type: Int8, object_id: Int32, metadata_id: Int32, values: SerializedObjectArray, meta_class_info):
        super().__init__(record_type, [object_id, metadata_id, values])
        self.__meta_class_info = meta_class_info

    @staticmethod
    def from_stream(stream: BinaryIO, class_info_dict: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]):
        """
            Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
            :param stream:
            :return:
        """
        record_type = Int8.from_stream(BytesIO(b"\x01"))
        object_id = Int32.from_stream(stream)
        metadata_id = Int32.from_stream(stream)

        class_info = class_info_dict[metadata_id.value()]
        values = load_values(stream, class_info, class_info_dict)
        return ClassWithID(record_type, object_id, metadata_id, values, class_info)

    def __repr__(self):
        return "ClassWithID"