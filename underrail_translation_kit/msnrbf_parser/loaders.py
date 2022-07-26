from io import BytesIO
from typing import BinaryIO, Tuple, Dict

from .enums import RecordType, BinaryType, PrimitiveType, BinaryArrayType
from .binary_object_string import BinaryObjectString
from .class_with_id import ClassWithID
from .class_with_members_and_types import ClassWithMembersAndTypes
from .system_class_with_members_and_types import SystemClassWithMembersAndTypes
from .misc_record_classes import MemberReference, BinaryArray, ArraySingleString
from .object_null import ObjectNull
from .primitives import RecordHeader, Int8, Int16, Int32, Double, KnickKnack, NoneObject
from .structure import ClassInfo, MemberTypeInfo, ClassTypeInfo
from .value_array import ValueArray

def load_values(stream: BinaryIO, class_info: Tuple[ClassInfo, MemberTypeInfo], class_info_dict: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]) -> ValueArray:
    items = []

    type_list = class_info[1].get_binary_type_list()
    primitive_type_list = class_info[1].get_primitive_enum_list()

    for i, type in enumerate(type_list):
        new_item = None
        if type == BinaryType.String:
            header = stream.read(1) # increment stream pointer
            if header == b"\x06":
                new_item = BinaryObjectString.from_stream(stream)
            elif header == b"\x09":
                new_item = MemberReference.from_stream(stream)
            else:
                raise Exception(f"unexpected header: {header}")

        elif type == BinaryType.Class:
            header = stream.read(1)  # increment stream pointer
            if header == b"\x01":   # 01_ClassWithID
                new_item = load_class_with_id(stream, class_info_dict)
            elif header == b"\x05":   # 05_ClassWithMembersAndTypes
                new_item = load_class_with_members_and_types(stream, class_info_dict)
            elif header == b"\x09":
                new_item = MemberReference.from_stream(stream)
            elif header == b"\x0A":     # objectnull
                new_item = ObjectNull()
            else:
                raise Exception(f"unexpected class header: {header}")
        elif type == BinaryType.Primitive:
            prim_type = primitive_type_list[i]
            if prim_type == PrimitiveType.Boolean:
                new_item = KnickKnack.from_stream(stream, 1, "Boolean")
            elif prim_type == PrimitiveType.Byte:
                new_item = Int8.from_stream(stream)
            elif prim_type == PrimitiveType.Int16:
                new_item = Int16.from_stream(stream)
            elif prim_type == PrimitiveType.Int32:
                new_item = Int32.from_stream(stream)
            elif prim_type == PrimitiveType.Int64:
                new_item = KnickKnack.from_stream(stream, 8, "Int64")
            elif prim_type == PrimitiveType.Double:
                new_item = Double.from_stream(stream)
            elif prim_type == PrimitiveType.Single:
                new_item = KnickKnack.from_stream(stream, 4, "Single")
            elif prim_type == PrimitiveType.UInt32:
                new_item = KnickKnack.from_stream(stream, 4, "UInt32")
            elif prim_type == PrimitiveType.TimeSpan:
                new_item = KnickKnack.from_stream(stream, 8, "TimeSpan")
            else:
                raise Exception(f"Not Implemented: {prim_type}")
        elif type == BinaryType.Object:
            header = stream.read(1)  # increment stream pointer
            assert header == b"\x0A"
            new_item = ObjectNull()
        elif type == BinaryType.StringArray:
            header = stream.read(1)
            if header == b"\x11":
                # TODO: duplication!
                new_item = ArraySingleString.from_stream(stream)
            elif header == b"\x09":
                new_item = MemberReference.from_stream(stream)
            else:
                raise Exception(f"unexpected header: {header}")
        elif type == BinaryType.SystemClass:
            header = stream.read(1)
            if header == b"\x04":
                new_item = load_system_class_with_members_and_types(stream, class_info_dict)
            elif header == b"\x09":
                new_item = MemberReference.from_stream(stream)
            else:
                raise Exception(f"unexpected header: {header}")
        else:
            raise Exception(f"Not Implemented: {type}")

        items.append(new_item)

    return ValueArray(items)

def load_system_class_with_members_and_types(stream: BinaryIO, class_info_dict: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]) -> SystemClassWithMembersAndTypes:
    """
        Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
    """
    record_type = RecordHeader(RecordType.SystemClassWithMembersAndTypes)
    class_info = ClassInfo.from_stream(stream)
    object_id = class_info.get_object_id()
    member_type_info = MemberTypeInfo.from_stream(stream, class_info.count())

    class_info_dict[object_id] = (class_info, member_type_info)

    values = load_values(stream, (class_info, member_type_info), class_info_dict)

    return SystemClassWithMembersAndTypes(record_type, class_info, member_type_info, values)

def load_class_with_members_and_types(stream: BinaryIO, class_info_dict: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]) -> ClassWithMembersAndTypes:

    record_type = RecordHeader(RecordType.ClassWithMembersAndTypes)
    class_info = ClassInfo.from_stream(stream)
    object_id = class_info.get_object_id()
    member_type_info = MemberTypeInfo.from_stream(stream, class_info.count())

    class_info_dict[object_id] = (class_info, member_type_info)

    library_id = Int32.from_stream(stream)
    values = load_values(stream, (class_info, member_type_info), class_info_dict)

    return ClassWithMembersAndTypes(record_type, class_info, member_type_info, library_id, values)

def load_class_with_id(stream: BinaryIO, class_info_dict: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]):
        record_type = RecordHeader(RecordType.ClassWithId)
        object_id = Int32.from_stream(stream)
        metadata_id = Int32.from_stream(stream)

        class_info = class_info_dict[metadata_id.value()]
        values = load_values(stream, class_info, class_info_dict)
        return ClassWithID(record_type, object_id, metadata_id, values, class_info)

def load_binary_array(stream: BinaryIO, class_info_dict: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]):
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

        # we do not implement for now
        #if binary_type == BinaryType.Object or binary_type == BinaryType.String or binary_type == BinaryType.ObjectArray or binary_type == BinaryType.StringArray:
        #    additional_type_info = NoneObject()
        #elif binary_type == BinaryType.Primitive:
        #    additional_type_info = KnickKnack.from_stream(stream, rank.value()*1)
        if binary_type == BinaryType.Class:
            additional_type_info = ClassTypeInfo.from_stream(stream)
            header = RecordHeader.from_stream(stream)
            if header.record_type == RecordType.ClassWithMembersAndTypes:
                values = load_class_with_members_and_types(stream, class_info_dict)
            else:
                raise Exception(f"Not implemented: {header.record_type}")
        else:
            raise Exception(f"Not implemented: {binary_type}")

        return BinaryArray(record_type, object_id, binary_array_type_enum, rank, lengths, lower_bounds, type_enum, additional_type_info, values)