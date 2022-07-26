from io import BytesIO
from typing import BinaryIO

from .primitives import Int8, Int32, LengthPrefixedString, KnickKnack
from .record import Record
from .serialized_object import SerializedObject

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