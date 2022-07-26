from typing import BinaryIO, List, Tuple, Dict

from underrail_translation_kit.msnrbf_parser.structure import ClassInfo, MemberTypeInfo
from .enums import RecordType
from .binary_object_string import BinaryObjectString
from .loaders import load_system_class_with_members_and_types, load_class_with_members_and_types, load_class_with_id, load_binary_array
from .misc_record_classes import SerializationHeader, BinaryLibrary, MessageEnd, ArraySingleString
from .parse_result import ParseResult

def parse_binary_stream(stream: BinaryIO) -> ParseResult:
    result = []
    class_info_dict: Dict[int, Tuple[ClassInfo, MemberTypeInfo]] = {}    # TODO: この実体はラッパクラスでいい まとめて使われることが多すぎる

    while (True):
        header = stream.read(1)
        record_type = RecordType(header[0])
        if len(header) == 0:
            raise Exception(f"the result is without MessageEnd record")

        new_item = None
        if record_type == RecordType.SerializedStreamHeader:
            new_item = SerializationHeader.from_stream(stream)
        elif record_type == RecordType.ClassWithId:
            new_item = load_class_with_id(stream, class_info_dict)
        elif record_type == RecordType.SystemClassWithMembersAndTypes:
            new_item = load_system_class_with_members_and_types(stream, class_info_dict)
        elif record_type == RecordType.ClassWithMembersAndTypes:
            new_item = load_class_with_members_and_types(stream, class_info_dict)
        elif record_type == RecordType.BinaryObjectString:
            new_item = BinaryObjectString.from_stream(stream)
        elif record_type == RecordType.BinaryArray:
            new_item = load_binary_array(stream, class_info_dict)
        elif record_type == RecordType.BinaryLibrary:
            new_item = BinaryLibrary.from_stream(stream)
        elif record_type == RecordType.ArraySingleString:
            new_item = ArraySingleString.from_stream(stream)
        elif record_type == RecordType.MessageEnd:
            result.append(MessageEnd())
            break
        else:
            raise Exception(f"not implemented: {record_type}")

        result.append(new_item)
        #print(new_item)

    return ParseResult(result)