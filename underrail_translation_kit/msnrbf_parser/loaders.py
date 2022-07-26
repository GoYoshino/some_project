from io import BytesIO
from typing import BinaryIO, List

from .binary_object_string import BinaryObjectString
from .class_with_members_and_types import ClassWithMembersAndTypes
from .enums import BinaryType, PrimitiveType
from .misc_record_classes import MemberReference
from .object_null import ObjectNull
from .primitives import Int8, Int16, Int32, Double
from .structure import ClassInfo, MemberTypeInfo
from .value_array import ValueArray

def load_values(stream: BinaryIO, type_list: List[BinaryType], primitive_type_list: List[PrimitiveType]) -> ValueArray:
    items = []
    for i, type in enumerate(type_list):
        new_item = None
        if type == BinaryType.String:
            header = stream.read(1) # increment stream pointer
            assert header == b"\x06"
            new_item = BinaryObjectString.from_stream(stream)
        elif type == BinaryType.Class:
            header = stream.read(1)  # increment stream pointer
            if header == b"\x05":
                new_item = load_class_with_members_and_types(stream)
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
            elif prim_type == PrimitiveType.Double:
                new_item = Double.from_stream(stream)
            else:
                raise Exception(f"Not Implemented: {prim_type}")
        elif type == BinaryType.Object:
            header = stream.read(1)  # increment stream pointer
            assert header == b"\x0A"
            new_item = ObjectNull()
        else:
            raise Exception(f"Not Implemented: {type}")

        items.append(new_item)

    return ValueArray(items)

def load_class_with_members_and_types(stream: BinaryIO) -> ClassWithMembersAndTypes:
    """
        Be sure that the pointer of stream is +1(after first byte of RecordTypeEnum)
        :param stream:
        :return:
    """
    record_type = Int8.from_stream(BytesIO(b"\x05"))
    class_info = ClassInfo.from_stream(stream)
    member_type_info = MemberTypeInfo.from_stream(stream, class_info.count())
    library_id = Int32.from_stream(stream)
    values = load_values(stream, member_type_info.get_binary_type_list(),
                        member_type_info.get_primitive_enum_list())

    return ClassWithMembersAndTypes(record_type, class_info, member_type_info, library_id, values)