from typing import BinaryIO

from .binary_object_string import BinaryObjectString
from .class_with_id import ClassWithID
from .loaders import load_class_with_members_and_types
from .misc_record_classes import SerializationHeader, BinaryLibrary, MessageEnd
from .parse_result import ParseResult
from .record import RecordType

def parse_binary_stream(stream: BinaryIO) -> ParseResult:
    result = []
    class_info_dict = {}

    while (True):
        header = stream.read(1)
        record_type = RecordType(header[0])
        if len(header) == 0:
            raise Exception(f"the result is without MessageEnd record")

        new_item = None
        if record_type == RecordType.SerializedStreamHeader:
            new_item = SerializationHeader.from_stream(stream)
        elif record_type == RecordType.ClassWithId:
            new_item = ClassWithID.from_stream(stream, class_info_dict)
        elif record_type == RecordType.ClassWithMembersAndTypes:
            new_item = load_class_with_members_and_types(stream, class_info_dict)
        elif record_type == RecordType.BinaryObjectString:
            new_item = BinaryObjectString.from_stream(stream)
        elif record_type == RecordType.BinaryLibrary:
            new_item = BinaryLibrary.from_stream(stream)
        elif record_type == RecordType.MessageEnd:
            result.append(MessageEnd())
            break
        else:
            raise Exception(f"not implemented: {record_type}")

        result.append(new_item)
        #print(new_item)

    return ParseResult(result)