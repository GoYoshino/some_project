from typing import List

from mock import Mock
import unittest

from underrail_translation_kit.msnrbf_parser.binary_object_string import BinaryObjectString
from underrail_translation_kit.msnrbf_parser.class_with_values import ClassWithValues
from underrail_translation_kit.msnrbf_parser.enums import BinaryType
from underrail_translation_kit.msnrbf_parser.object_null import ObjectNull
from underrail_translation_kit.msnrbf_parser.primitives import RecordType, RecordHeader
from underrail_translation_kit.msnrbf_parser.structure import ClassInfo, MemberTypeInfo
from underrail_translation_kit.msnrbf_parser.value_array import ValueArray


class ClassWithMembersTest(unittest.TestCase):

    def fabricate_mock_member_type_info(self, values: ValueArray) -> MemberTypeInfo:
        result: List[BinaryType] = []
        for value in values.items:
            if isinstance(value, BinaryObjectString):
                result.append(BinaryType.String)
            elif isinstance(value, ObjectNull):
                result.append(BinaryType.Object)
            else:
                self.fail(f"not implemented for object: {value}")

        member_type_info = Mock(MemberTypeInfo)
        member_type_info.raw_bytes = "めんた".encode("utf-8")
        member_type_info.get_binary_type_list.return_value = result

        return member_type_info

    def test_get_text_direct_child(self):
        record_header = RecordHeader(RecordType.ClassWithMembersAndTypes)
        class_info = Mock(ClassInfo)
        class_info.raw_bytes = "いんふぉ".encode("utf-8")

        target_string = BinaryObjectString.from_params(32, "abcdefg")
        values = ValueArray([ObjectNull(), target_string, ObjectNull()])
        member_type_info = self.fabricate_mock_member_type_info(values)

        subject = ClassWithValues(record_header, class_info, member_type_info, [], values)

        self.assertEqual("abcdefg", subject.get_text(32))

    def test_get_text_recursively(self):
        pass

    def test_replace_text_diret_child(self):
        pass

    def test_replace_text_recursively(self):
        pass

if __name__ == '__main__':
    unittest.main()
