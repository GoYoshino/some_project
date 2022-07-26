from io import BytesIO
from typing import BinaryIO, Tuple, Dict

from .binary_object_string import BinaryObjectString
from .class_with_id import ClassWithID
from .class_with_members_and_types import ClassWithMembersAndTypes
from .enums import BinaryType, PrimitiveType, BinaryArrayType
from .misc_record_classes import MemberReference, BinaryArray, ArraySingleString
from .object_null import ObjectNull
from .primitives import Int8, Int16, Int32, Double, KnickKnack, NoneObject
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
            assert header == b"\x06"
            new_item = BinaryObjectString.from_stream(stream)
        elif type == BinaryType.Class:
            header = stream.read(1)  # increment stream pointer
            if header == b"\x01":   # 01_ClassWithID
                new_item = load_class_with_id(stream, class_info_dict)
            elif header == b"\x05":   # 05_ClassWithMembersAndTypes
                new_item = load_class_with_members_and_types(stream, class_info_dict)
            elif header == b"\x09":
                new_item = MemberReference.from_stream(stream)
            else:
                raise Exception(f"unexpected class header: {header}")
        elif type == BinaryType.Primitive:
            prim_type = primitive_type_list[i]
            if prim_type == PrimitiveType.Boolean:
                new_item = Int8.from_stream(stream)
            elif prim_type == PrimitiveType.Int16:
                new_item = Int16.from_stream(stream)
            elif prim_type == PrimitiveType.Int32:
                new_item = Int32.from_stream(stream)
            elif prim_type == PrimitiveType.Int64:
                new_item = KnickKnack.from_stream(stream, 8)
            elif prim_type == PrimitiveType.Double:
                new_item = Double.from_stream(stream)
            elif prim_type == PrimitiveType.Single:
                new_item = KnickKnack.from_stream(stream, 4)
            else:
                raise Exception(f"Not Implemented: {prim_type}")
        elif type == BinaryType.Object:
            header = stream.read(1)  # increment stream pointer
            assert header == b"\x0A"
            new_item = ObjectNull()
        elif type == BinaryType.StringArray:
            new_item = ArraySingleString
        else:
            raise Exception(f"Not Implemented: {type}")

        items.append(new_item)

    return ValueArray(items)

def load_class_with_members_and_types(stream: BinaryIO, class_info_dict: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]) -> ClassWithMembersAndTypes:
    """
        Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
        :param stream:
        :return:
    """
    record_type = Int8.from_stream(BytesIO(b"\x05"))
    class_info = ClassInfo.from_stream(stream)
    object_id = class_info.get_object_id()
    member_type_info = MemberTypeInfo.from_stream(stream, class_info.count())

    class_info_dict[object_id] = (class_info, member_type_info)

    library_id = Int32.from_stream(stream)
    values = load_values(stream, (class_info, member_type_info), class_info_dict)

    return ClassWithMembersAndTypes(record_type, class_info, member_type_info, library_id, values)

def load_class_with_id(stream: BinaryIO, class_info_dict: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]):
        record_type = Int8.from_stream(BytesIO(b"\x01"))
        object_id = Int32.from_stream(stream)
        metadata_id = Int32.from_stream(stream)

        class_info = class_info_dict[metadata_id.value()]
        values = load_values(stream, class_info, class_info_dict)
        return ClassWithID(record_type, object_id, metadata_id, values, class_info)

def load_binary_array(stream: BinaryIO, class_info_dict: Dict[int, Tuple[ClassInfo, MemberTypeInfo]]):
        record_type = Int8.from_stream(BytesIO(b"\x07"))
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
            # TODO: header check code is duplicated. can be externalized later
            header = Int8.from_stream(stream)
            if header.raw_bytes == b"\x05":
                values = load_class_with_members_and_types(stream, class_info_dict)
            else:
                raise Exception(f"Not implemented: {header}")
        else:
            raise Exception(f"Not implemented: {binary_type}")

        return BinaryArray(record_type, object_id, binary_array_type_enum, rank, lengths, lower_bounds, type_enum, additional_type_info, values)