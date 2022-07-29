from typing import BinaryIO, Dict, List, Optional

from underrail_translation_kit.msnrbf_parser.record_with_values import RecordWithValues
from .binary_object_string import BinaryObjectString
from .enums import RecordType
from .object_null import ObjectNull
from .length_prefixed_string import LengthPrefixedString
from .primitives import Int8, Int32, RecordHeader, KnickKnack
from .record import Record
from .serialized_object import SerializedObject
from .serialized_object_array import SerializedObjectArray
from .structure import ArrayInfo

class SerializationHeader(Record):
    """
    Refers to 00: SerializationHeader Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    Because header has nothing to do with translation work
    """

    def __init__(self, record_header: RecordHeader, root_id: Int32, header_id: Int32, major_version: Int32, minor_version: Int32):
        super().__init__(record_header, [root_id, header_id, major_version, minor_version])

    @staticmethod
    def from_stream(stream: BinaryIO):
        """
        Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
        :param stream:
        :return:
        """
        record_header = RecordHeader(RecordType.SerializedStreamHeader)
        root_id = Int32.from_stream(stream)
        header_id = Int32.from_stream(stream)
        major_version = Int32.from_stream(stream)
        minor_version = Int32.from_stream(stream)
        return SerializationHeader(record_header, root_id, header_id, major_version, minor_version)

    def __repr__(self):
        return "SerializationHeader"

class BinaryArray(Record):
    """
    Refers to 07: MemberReference Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    Because header has nothing to do with translation work
    """

    def __init__(self, record_header: RecordHeader, object_id: Int32,
                 binary_array_type_enum: Int8, rank: Int32, lengths: KnickKnack, lower_bounds: SerializedObject,
                 type_enum: Int8, additional_type_info: KnickKnack, values: SerializedObjectArray):
        super().__init__(record_header,
                         [ object_id,
                           binary_array_type_enum, rank, lengths, lower_bounds,
                           type_enum, additional_type_info, values ])


class MemberReference(Record):
    """
    Refers to 09: MemberReference Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    Because header has nothing to do with translation work
    """

    def __init__(self, record_header: RecordHeader, id_ref: Int32):
        super().__init__(record_header, [id_ref])

    @staticmethod
    def from_stream(stream: BinaryIO):
        record_header = RecordHeader(RecordType.MemberReference)
        id_ref = Int32.from_stream(stream)
        return MemberReference(record_header, id_ref)


class MessageEnd(Record):
    """
    Refers to 0B: MessageEnd Record
    """

    def __init__(self):
        record_header = RecordHeader(RecordType.MessageEnd)
        super().__init__(record_header, [])

class BinaryLibrary(Record):
    """
    Refers to 0C: BinaryLibrary Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    Because header has nothing to do with translation work
    """

    def __init__(self, record_header: RecordHeader, library_id: Int32, library_name: LengthPrefixedString):
        super().__init__(record_header, [library_id, library_name])

    @staticmethod
    def from_stream(stream: BinaryIO):
        """
            Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
            :param stream:
            :param record_type:
            :return:
        """
        record_type = RecordHeader(RecordType.BinaryLibrary)
        library_id = Int32.from_stream(stream)
        library_name = LengthPrefixedString.from_stream(stream)
        return BinaryLibrary(record_type, library_id, library_name)

    def __repr__(self):
        return "BinaryLibrary"


class ArraySingleString(Record, RecordWithValues):
    """
    Refers to 11(17): ArraySingleString Record
    """
    def __init__(self, record_header: RecordHeader, array_info: ArrayInfo, values: SerializedObjectArray, string_values_dict: Dict[int, BinaryObjectString]):
        super().__init__(record_header, [array_info, values])
        self.__array_info = array_info
        self.__string_values_dict = string_values_dict

    @staticmethod
    def from_stream(stream: BinaryIO):
        record_header = RecordHeader(RecordType.ArraySingleString)
        array_info = ArrayInfo.from_stream(stream)
        length = array_info.get_length()

        values = []
        string_values = {}
        remaining_null_objects = 0
        for i in range(length):
            if (remaining_null_objects > 0):
                remaining_null_objects -= 1
                continue
            # TODO: 古い実装を直す
            header = Int8.from_stream(stream)
            if header.raw_bytes == b"\x06":
                value = BinaryObjectString.from_stream(stream)
                value_object_id = value.get_object_id()
                string_values[value_object_id] = value
                values.append(value)
            elif header.raw_bytes == b"\x0A":
                values.append(ObjectNull())
            elif header.raw_bytes == b"\x0D":   # 0D_ObjectNullMultiple256
                object_null = ObjectNullMultiple256.from_stream(stream)
                values.append(object_null)
                remaining_null_objects += object_null.get_count()
            else:
                raise Exception(f"Unexpected header: {header}")

        return ArraySingleString(record_header, array_info, SerializedObjectArray(values), string_values)

    @staticmethod
    def fabricate(object_id: int, values: List[BinaryObjectString]):
        dictionary = {}
        for value in values:
            dictionary[value.get_object_id()] = value
        return ArraySingleString(
            RecordHeader(RecordType.ArraySingleString),
            ArrayInfo(Int32.from_value(object_id), Int32.from_value(len(values))),
            SerializedObjectArray(values),
            dictionary
        )


    def get_object_id(self) -> int:
        return self.__array_info.get_object_id()

    def get_name(self):
        return "array"

    def has_bos_as_direct_child(self, object_id: int) -> bool:
        return object_id in self.__string_values_dict.keys()

    def get_bos_recursively(self, object_id: int) -> Optional[BinaryObjectString]:
        if object_id in self.__string_values_dict:
            return self.__string_values_dict[object_id]
        else:
            return None

    def get_string(self, object_id: int) -> BinaryObjectString:
        return self.__string_values_dict[object_id]

    def get_direct_child_string_member_dict(self) -> Dict[int, BinaryObjectString]:
        return self.__string_values_dict

    def find_text(self, object_id: int) -> str:
        return self.get_string(object_id).get_string()

    def replace_text(self, new_string: str, object_id: int) -> None:
        self.get_string(object_id).replace_string(new_string)

    def get_all_texts(self) -> Dict[int, BinaryObjectString]:
        return self.__string_values_dict


class ObjectNullMultiple256(Record):
    """
    Refers to 0D: ObjectNullMultiple256 Record
    """

    def __init__(self, record_header: RecordHeader, null_count: Int8):
        super().__init__(record_header, [null_count])
        self.__count = null_count

    def get_count(self) -> int:
        return self.__count.value()

    @staticmethod
    def from_stream(stream: BinaryIO):
        record_type = RecordHeader(RecordType.ObjectNullMultiple256)
        null_count = Int8.from_stream(stream)
        return ObjectNullMultiple256(record_type, null_count)