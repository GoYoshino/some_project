import logging
from typing import BinaryIO, List
from msnrbf.records.record import RecordType, Record, BinaryLibrary
from msnrbf.core.serialized_object import SerializedObject, LengthPrefixedString, Int8, Int32

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def __parseFixedLengthRecord(handle: BinaryIO, header: bytes, length: int) -> Record:

    # does not provide any decoding functionality because the record has nothing to do with translation work

    payload = handle.read(length)
    raw_bytes = header + payload

    return Record(raw_bytes, RecordType(int.from_bytes(header, "little")))

def __parseBinaryLibrary(handle: BinaryIO, header: bytes) -> BinaryLibrary:
    assert len(header) == 1
    library_id = Int32.fromStream(handle)
    library_name = LengthPrefixedString.fromStream(handle)

    return BinaryLibrary(library_id, library_name)

def __parseClassWithID(handle: BinaryIO, header: bytes) -> Record:
    assert len(header) == 1
    bytes_object_id = handle.read(4)
    bytes_metadata_id = handle.read(4)
    raw_bytes = header + bytes_object_id + bytes_metadata_id
    return Record(raw_bytes, RecordType.ClassWithId)

def parse(handle: BinaryIO) -> List[Record]:

    result = []

    while True:
        header = handle.read(1)

        newRecord = None
        record_type = RecordType(int.from_bytes(header, "little"))
        if record_type == RecordType.SerializedStreamHeader:
            newRecord = __parseFixedLengthRecord(handle, header, 16)
        elif record_type == RecordType.ClassWithId:
            newRecord = __parseFixedLengthRecord(handle, header, 8)
        elif record_type == RecordType.BinaryLibrary:
            newRecord = __parseBinaryLibrary(handle, header)
        else:
            raise Exception(f"incompatible record type: {record_type}")
        result.append(newRecord)
        print(newRecord)

        if record_type == RecordType.MessageEnd:
            break

    return result