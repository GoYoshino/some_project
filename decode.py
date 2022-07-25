from typing import BinaryIO, List

from core.binary_object_string import BinaryObjectString
from core.class_with_members_and_types import ClassWithMembersAndTypes
from core.serialized_object_array import SerializedObjectArray
from core.record import RecordType
from core.record_classes import SerializationHeader, BinaryLibrary, MessageEnd
from core.loaders import load_class_with_members_and_types

def decode(stream: BinaryIO) -> SerializedObjectArray:
    result = []

    while (True):
        header = stream.read(1)
        record_type = RecordType(header[0])
        if len(header) == 0:
            raise Exception(f"the result is without MessageEnd record")

        new_item = None
        if record_type == RecordType.SerializedStreamHeader:
            new_item = SerializationHeader.from_stream(stream)
        #elif record_type == RecordType.ClassWithId:
        #    new_item = ClassWithId.from_stream(stream)
        elif record_type == RecordType.ClassWithMembersAndTypes:
            new_item = load_class_with_members_and_types(stream)
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
        print(new_item)

    return SerializedObjectArray(result)