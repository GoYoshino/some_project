from io import BytesIO
from typing import BinaryIO, Tuple, Dict

from .binary_object_string import BinaryObjectString
from .class_with_members_and_types import ClassWithMembersAndTypes
from .enums import BinaryType, PrimitiveType
from .misc_record_classes import MemberReference
from .object_null import ObjectNull
from .primitives import Int8, Int16, Int32, Double, KnickKnack
from .structure import ClassInfo, MemberTypeInfo
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
            if header == b"\x05":   # 05_ClassWithMembersAndTypes
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