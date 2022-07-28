from underrail_translation_kit.msnrbf_parser.class_with_values import ClassWithValues
from underrail_translation_kit.msnrbf_parser.structure import MemberTypeInfo, ClassInfo
from underrail_translation_kit.msnrbf_parser.value_array import ValueArray
from .primitives import RecordHeader, Int32


class ClassWithID(ClassWithValues):
    """
        Refers to 01: ClassWithID Record
        Does not care detailed behavior as long as the instance preserves original raw byte array
        Because header has nothing to do with translation work
        """

    def __init__(self, record_header: RecordHeader, object_id: Int32, metadata_id: Int32, values: ValueArray, meta_class_info: ClassInfo, meta_member_type_info: MemberTypeInfo):
        super().__init__(record_header, meta_class_info, meta_member_type_info, [object_id, metadata_id], values)

    def __repr__(self):
        return "ClassWithID"