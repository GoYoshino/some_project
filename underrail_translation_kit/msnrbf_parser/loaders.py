from typing import BinaryIO, Tuple, Dict, List

from .enums import RecordType, BinaryType, PrimitiveType, BinaryArrayType
from .binary_object_string import BinaryObjectString
from .class_with_id import ClassWithID
from .class_with_members_and_types import ClassWithMembersAndTypes
from .system_class_with_members_and_types import SystemClassWithMembersAndTypes
from .misc_record_classes import MemberReference, BinaryArray, ArraySingleString
from .object_null import ObjectNull
from .primitives import RecordHeader, Int8, Int16, Int32, Double, KnickKnack, NoneObject
from .serialized_object import SerializedObject
from .structure import ClassInfo, MemberTypeInfo, ClassTypeInfo
from .value_array import ValueArray


def _load_string_value(stream: BinaryIO) -> SerializedObject:
    header = RecordHeader.from_stream(stream)
    if header.record_type == RecordType.BinaryObjectString:
        return BinaryObjectString.from_stream(stream)
    elif header.record_type == RecordType.MemberReference:
        return MemberReference.from_stream(stream)
    else:
        raise Exception(f"unexpected header: {header}")


def _load_class_value(stream: BinaryIO, class_info_dict: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]) -> SerializedObject:
    header = RecordHeader.from_stream(stream)
    if header.record_type == RecordType.ClassWithId:
        return load_class_with_id(stream, class_info_dict)
    elif header.record_type == RecordType.ClassWithMembersAndTypes:
        return load_class_with_members_and_types(stream, class_info_dict)
    elif header.record_type == RecordType.MemberReference:
        return MemberReference.from_stream(stream)
    elif header.record_type == RecordType.ObjectNull:
        return ObjectNull()
    else:
        raise Exception(f"unexpected class header: {header}")


def _load_primitive_value(stream: BinaryIO, primitive_type: PrimitiveType):
    if primitive_type == PrimitiveType.Boolean:
        return KnickKnack.from_stream(stream, 1, "Boolean")
    elif primitive_type == PrimitiveType.Byte:
        return Int8.from_stream(stream)
    elif primitive_type == PrimitiveType.Int16:
        return Int16.from_stream(stream)
    elif primitive_type == PrimitiveType.Int32:
        return Int32.from_stream(stream)
    elif primitive_type == PrimitiveType.Int64:
        return KnickKnack.from_stream(stream, 8, "Int64")
    elif primitive_type == PrimitiveType.Double:
        return Double.from_stream(stream)
    elif primitive_type == PrimitiveType.Single:
        return KnickKnack.from_stream(stream, 4, "Single")
    elif primitive_type == PrimitiveType.UInt32:
        return KnickKnack.from_stream(stream, 4, "UInt32")
    elif primitive_type == PrimitiveType.TimeSpan:
        return KnickKnack.from_stream(stream, 8, "TimeSpan")
    else:
        raise Exception(f"Not Implemented: {primitive_type}")


def _load_object_value(stream: BinaryIO) -> SerializedObject:
    header = stream.read(1)  # increment stream pointer
    assert header == b"\x0A"
    return ObjectNull()


def _load_string_array_value(stream: BinaryIO) -> SerializedObject:
    header = stream.read(1)
    if header == b"\x11":
        return ArraySingleString.from_stream(stream)
    elif header == b"\x09":
        return MemberReference.from_stream(stream)
    else:
        raise Exception(f"unexpected header: {header}")


def _load_system_class_value(stream: BinaryIO, class_info_appeared_so_far: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]) -> SerializedObject:
    header = stream.read(1)
    if header == b"\x04":
        return load_system_class_with_members_and_types(stream, class_info_appeared_so_far)
    elif header == b"\x09":
        return MemberReference.from_stream(stream)
    else:
        raise Exception(f"unexpected header: {header}")


def load_values(stream: BinaryIO, class_info: Tuple[ClassInfo, MemberTypeInfo], class_info_appeared_so_far: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]) -> ValueArray:
    items = []

    type_list = class_info[1].get_binary_type_list()
    primitive_type_list = class_info[1].get_primitive_enum_list()

    for i, type in enumerate(type_list):
        new_item = None
        if type == BinaryType.String:
            new_item = _load_string_value(stream)
        elif type == BinaryType.SystemClass:
            new_item = _load_system_class_value(stream, class_info_appeared_so_far)
        elif type == BinaryType.Class:
            new_item = _load_class_value(stream, class_info_appeared_so_far)
        elif type == BinaryType.Primitive:
            new_item = _load_primitive_value(stream, primitive_type_list[i])
        elif type == BinaryType.Object:
            new_item = _load_object_value(stream)
        elif type == BinaryType.StringArray:
            new_item = _load_string_value(stream)
        else:
            raise Exception(f"Not Implemented: {type}")

        items.append(new_item)

    return ValueArray(items)

def load_system_class_with_members_and_types(stream: BinaryIO, class_info_appeared_so_far: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]) -> SystemClassWithMembersAndTypes:
    """
        Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
    """
    record_type = RecordHeader(RecordType.SystemClassWithMembersAndTypes)
    class_info = ClassInfo.from_stream(stream)
    object_id = class_info.get_object_id()
    member_type_info = MemberTypeInfo.from_stream(stream, class_info.count())

    class_info_appeared_so_far[object_id] = (class_info, member_type_info)

    values = load_values(stream, (class_info, member_type_info), class_info_appeared_so_far)

    return SystemClassWithMembersAndTypes(record_type, class_info, member_type_info, values)


def load_class_with_members_and_types(stream: BinaryIO, class_info_appeared_so_far: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]) -> ClassWithMembersAndTypes:

    record_type = RecordHeader(RecordType.ClassWithMembersAndTypes)
    class_info = ClassInfo.from_stream(stream)
    object_id = class_info.get_object_id()
    member_type_info = MemberTypeInfo.from_stream(stream, class_info.count())

    class_info_appeared_so_far[object_id] = (class_info, member_type_info)

    library_id = Int32.from_stream(stream)
    values = load_values(stream, (class_info, member_type_info), class_info_appeared_so_far)

    return ClassWithMembersAndTypes(record_type, class_info, member_type_info, library_id, values)


def load_class_with_id(stream: BinaryIO, class_info_appeared_so_far: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]):
        record_type = RecordHeader(RecordType.ClassWithId)
        object_id = Int32.from_stream(stream)
        metadata_id = Int32.from_stream(stream)

        class_info = class_info_appeared_so_far[metadata_id.value()]
        values = load_values(stream, class_info, class_info_appeared_so_far)
        return ClassWithID(record_type, object_id, metadata_id, values, class_info)


def load_binary_array(stream: BinaryIO, class_info_appeared_so_far: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]):
        record_type = RecordHeader(RecordType.BinaryArray)
        object_id = Int32.from_stream(stream)
        binary_array_type_enum = Int8.from_stream(stream)
        rank = Int32.from_stream(stream)
        lengths = KnickKnack.from_stream(stream, rank.value()*4)

        array_type = BinaryArrayType(binary_array_type_enum.value())
        if (array_type == BinaryArrayType.SingleOffset
            or array_type == BinaryArrayType.JaggedOffset
            or array_type == BinaryArrayType.RectangularOffset):
            lower_bounds = KnickKnack.from_stream(stream, rank.value()*4)
        else:
            lower_bounds = NoneObject()

        type_enum = Int8.from_stream(stream)

        binary_type = BinaryType(type_enum.value())

        ### AdditionalInfo ###
        additional_type_info = None
        # we do not implement for now
        #if binary_type == BinaryType.Object or binary_type == BinaryType.String or binary_type == BinaryType.ObjectArray or binary_type == BinaryType.StringArray:
        #    additional_type_info = NoneObject()
        #elif binary_type == BinaryType.Primitive:
        #    additional_type_info = KnickKnack.from_stream(stream, rank.value()*1)
        if binary_type == BinaryType.Class:
            additional_type_info = ClassTypeInfo.from_stream(stream)
        else:
            Exception(f"Not implemented: {binary_type}")

        ### Values ###
        # NO values for 0-rank arrays / 0-length arrays
        if rank.value() == 0 or (rank.value() == 1 and int.from_bytes(lengths.raw_bytes, "little") == 0):
            values = NoneObject()
            return BinaryArray(record_type, object_id, binary_array_type_enum, rank, lengths, lower_bounds, type_enum, additional_type_info, values)

        header = RecordHeader.from_stream(stream)
        if header.record_type == RecordType.ClassWithMembersAndTypes:
            values = load_class_with_members_and_types(stream, class_info_appeared_so_far)
        elif header.record_type == RecordType.ClassWithId:
            values = load_class_with_id(stream, class_info_appeared_so_far)
        else:
            print(record_type.raw_bytes + object_id. raw_bytes + binary_array_type_enum.raw_bytes + rank.raw_bytes + lengths.raw_bytes)
            raise Exception(f"Not implemented: {header.record_type}")

        return BinaryArray(record_type, object_id, binary_array_type_enum, rank, lengths, lower_bounds, type_enum, additional_type_info, values)
