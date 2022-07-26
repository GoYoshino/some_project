from io import BytesIO
from typing import BinaryIO

from .binary_object_string import BinaryObjectString
from .primitives import Int8, Int32, LengthPrefixedString, KnickKnack, NoneObject
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

    def __init__(self, record_type: Int8, root_id: Int32, header_id: Int32, major_version: Int32, minor_version: Int32):
        super().__init__(record_type, [root_id, header_id, major_version, minor_version])

    @staticmethod
    def from_stream(stream: BinaryIO):
        """
        Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
        :param stream:
        :return:
        """
        record_type = Int8.from_stream(BytesIO(b"\x00"))
        root_id = Int32.from_stream(stream)
        header_id = Int32.from_stream(stream)
        major_version = Int32.from_stream(stream)
        minor_version = Int32.from_stream(stream)
        return SerializationHeader(record_type, root_id, header_id, major_version, minor_version)

    def __repr__(self):
        return "SerializationHeader"

class BinaryArray(Record):
    """
    Refers to 07: MemberReference Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    Because header has nothing to do with translation work
    """

    def __init__(self, record_type: Int8, object_id: Int32,
                 binary_array_type_enum: Int8, rank: Int32, lengths: KnickKnack, lower_bounds: KnickKnack,
                 type_enum: Int8, additional_type_info: KnickKnack, values: SerializedObject):
        super().__init__(record_type,
                         [ object_id,
                           binary_array_type_enum, rank, lengths, lower_bounds,
                           type_enum, additional_type_info, values ])


class MemberReference(Record):
    """
    Refers to 09: MemberReference Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    Because header has nothing to do with translation work
    """

    def __init__(self, record_type: Int8, id_ref: Int32):
        super().__init__(record_type, [ id_ref ])

    @staticmethod
    def from_stream(stream: BinaryIO):
        record_type = Int8.from_stream(BytesIO(b"\x09"))
        id_ref = Int32.from_stream(stream)
        return MemberReference(record_type, id_ref)


class MessageEnd(Record):
    """
    Refers to 0B: MessageEnd Record
    """

    def __init__(self):
        record_type = Int8.from_stream(BytesIO(b"\x0B"))
        super().__init__(record_type, [])

class BinaryLibrary(Record):
    """
    Refers to 0C: BinaryLibrary Record
    Does not care detailed behavior as long as the instance preserves original raw byte array
    Because header has nothing to do with translation work
    """

    def __init__(self, record_type: Int8, library_id: Int32, library_name: LengthPrefixedString):
        super().__init__(record_type, [library_id, library_name])

    @staticmethod
    def from_stream(stream: BinaryIO):
        """
            Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
            :param stream:
            :param record_type:
            :return:
        """
        record_type = Int8.from_stream(BytesIO(b"\x0C"))
        library_id = Int32.from_stream(stream)
        library_name = LengthPrefixedString.from_stream(stream)
        return BinaryLibrary(record_type, library_id, library_name)

    def __repr__(self):
        return "BinaryLibrary"

class ArraySingleString(Record):
    """
    Refers to 11(17): ArraySingleString Record
    """
    def __init__(self, record_type: Int8, array_info: ArrayInfo, values: SerializedObjectArray):
        super().__init__(record_type, [array_info, values])

    @staticmethod
    def from_stream(stream: BinaryIO):
        record_type = Int8.from_stream(BytesIO(b"\x11"))
        array_info = ArrayInfo.from_stream(stream)
        length = array_info.get_length()

        values = []
        remaining_null_objects = 0
        for i in range(length):
            if (remaining_null_objects > 0):
                remaining_null_objects -= 1
                continue
            header = Int8.from_stream(stream)
            if header.raw_bytes == b"\x06":
                values.append(BinaryObjectString.from_stream(stream))
            elif header.raw_bytes == b"\x0A":
                values.append(NoneObject())
            elif header.raw_bytes == b"\x0D":   # 0D_ObjectNullMultiple256
                object_null = ObjectNullMultiple256.from_stream(stream)
                values.append(object_null)
                remaining_null_objects += object_null.get_count()
            else:
                raise Exception(f"Unexpected header: {header}")

        return ArraySingleString(record_type, array_info, SerializedObjectArray(values))


class ObjectNullMultiple256(Record):
    """
    Refers to 0D: ObjectNullMultiple256 Record
    """

    def __init__(self, record_type: Int8, null_count: Int8):
        super().__init__(record_type, [null_count])
        self.__count = null_count

    def get_count(self) -> int:
        return self.__count.value()

    @staticmethod
    def from_stream(stream: BinaryIO):
        # TODO: このfrom_streamみたいなやつを直で生成できるIFを作る
        record_type = Int8.from_stream(BytesIO(b"\x0D"))
        null_count = Int8.from_stream(stream)
        return ObjectNullMultiple256(record_type, null_count)