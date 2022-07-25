from typing import BinaryIO, List

from core.serialized_object_array import SerializedObjectArray
from core.record import Record, RecordType, SerializationHeader, ClassWithMembersAndTypes, BinaryObjectString, BinaryLibrary, MessageEnd

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
        elif record_type == RecordType.ClassWithMembersAndTypes:
            new_item = ClassWithMembersAndTypes.from_stream(stream)
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