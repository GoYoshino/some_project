from typing import List, Tuple

from mock import Mock
import unittest

from underrail_translation_kit.msnrbf_parser.binary_object_string import BinaryObjectString
from underrail_translation_kit.msnrbf_parser.class_with_members_and_types import ClassWithMembersAndTypes
from underrail_translation_kit.msnrbf_parser.class_with_values import ClassWithValues
from underrail_translation_kit.msnrbf_parser.enums import BinaryType
from underrail_translation_kit.msnrbf_parser.misc_record_classes import ArraySingleString
from underrail_translation_kit.msnrbf_parser.object_null import ObjectNull
from underrail_translation_kit.msnrbf_parser.primitives import RecordType, RecordHeader, Int32
from underrail_translation_kit.msnrbf_parser.serialized_object import SerializedObject
from underrail_translation_kit.msnrbf_parser.structure import ClassInfo, MemberTypeInfo
from underrail_translation_kit.msnrbf_parser.value_array import ValueArray


class ClassWithMembersTest(unittest.TestCase):

    # TODO: 汚いテストを書き直す
    def fabricate_mock_member_type_info(self, values: ValueArray) -> MemberTypeInfo:
        result: List[BinaryType] = []
        for value in values.items:
            if isinstance(value, BinaryObjectString):
                result.append(BinaryType.String)
            elif isinstance(value, ObjectNull):
                result.append(BinaryType.Object)
            elif isinstance(value, ClassWithValues):
                result.append(BinaryType.Class)
            elif isinstance(value, ArraySingleString):
                result.append(BinaryType.StringArray)
            else:
                self.fail(f"not implemented for object: {value}")

        member_type_info = Mock(MemberTypeInfo)
        member_type_info.raw_bytes = "めんた".encode("utf-8")
        member_type_info.get_binary_type_list.return_value = result

        return member_type_info

    def fabricate_knickknacks(self) -> Tuple[RecordHeader, ClassInfo]:
        record_header = RecordHeader(RecordType.ClassWithMembersAndTypes)
        class_info = Mock(ClassInfo)
        class_info.raw_bytes = "いんふぉ".encode("utf-8")

        return record_header, class_info

    def fabricate_with(self, object_id: int, value_list: List[SerializedObject]) -> ClassWithValues:
        record_header, class_info = self.fabricate_knickknacks()

        values = ValueArray(value_list)
        class_info = Mock(ClassInfo)
        class_info.get_object_id.return_value = object_id
        class_info.raw_bytes = b"mockclassinfo"
        member_type_info = self.fabricate_mock_member_type_info(values)

        return ClassWithMembersAndTypes(record_header, class_info, member_type_info, Int32.from_value(1), values)

    def test_has_nekochan(self):
        subject = self.fabricate_with(1001, [
            BinaryObjectString.from_params(27, "ﾈｺﾁｬﾝ"),
            BinaryObjectString.from_params(32, "ｲﾇﾁｬﾝ"),
            BinaryObjectString.from_params(14, "ｶﾜｳｿﾁｬﾝ")
        ])

        self.assertTrue(subject.has_bos_as_direct_child(27))

    def test_has_nekochan_in_child(self):
        nekochan_cage = Mock(ClassWithValues)
        nekochan_cage.has_bos_as_direct_child.return_value = True
        nekochan_cage.get_bos_recursively.return_value = BinaryObjectString.from_params(27, "ﾈｺﾁｬﾝ")
        nekochan_cage.get_object_id.return_value = 1001
        nekochan_cage.raw_bytes = b"neko"
        subject = self.fabricate_with(1002, [
            nekochan_cage,
            BinaryObjectString.from_params(32, "ｲﾇﾁｬﾝ"),
            BinaryObjectString.from_params(14, "ｶﾜｳｿﾁｬﾝ")
        ])

        self.assertFalse(subject.has_bos_as_direct_child(27))
        self.assertTrue(subject.has_bos_recursively(27))

    def test_get_nekochan_the_grandson(self):
        nekochan_cage = Mock(ClassWithValues)
        nekochan_cage.has_bos_as_direct_child.return_value = True
        nekochan_cage.raw_bytes = b"Nekochan_The_Grandson"
        nekochan_cage.get_bos_recursively.return_value = BinaryObjectString.from_params(27, "Nekochan The Grandson")
        nekochan_cage.get_object_id.return_value = 1001

        nekochan_house = self.fabricate_with(1002, [
            nekochan_cage,
            BinaryObjectString.from_params(33, "カリカリ")
        ])

        self.assertFalse(nekochan_house.has_bos_as_direct_child(27))
        self.assertTrue(nekochan_house.has_bos_recursively(27))

    def test_no_nekochan(self):
        subject = self.fabricate_with(1000, [
            BinaryObjectString.from_params(32, "ｲﾇﾁｬﾝ"),
            BinaryObjectString.from_params(14, "ｶﾜｳｿﾁｬﾝ")
        ])

        self.assertFalse(subject.has_bos_as_direct_child(27))

    # TODO: あとでけす　directchildかそうでないかの区別は不要
    def test_i_SAID_no_nekochan(self):
        record_header, class_info = self.fabricate_knickknacks()

        inu = BinaryObjectString.from_params(32, "ｲﾇﾁｬﾝ")
        kawauso = BinaryObjectString.from_params(14, "ｶﾜｳｿﾁｬﾝ")
        values = ValueArray([ObjectNull(), inu, kawauso ])
        member_type_info = self.fabricate_mock_member_type_info(values)
        subject = ClassWithValues(record_header, class_info, member_type_info, [], values)

        with self.assertRaises(Exception):
            subject.find_text(27)

    def test_get_text_direct_child(self):
        record_header, class_info = self.fabricate_knickknacks()

        target_string = BinaryObjectString.from_params(32, "abcdefg")
        different_string = BinaryObjectString.from_params(14, "ああああ")
        values = ValueArray([ObjectNull(), target_string, ObjectNull(), different_string])
        member_type_info = self.fabricate_mock_member_type_info(values)

        subject = ClassWithValues(record_header, class_info, member_type_info, [], values)

        self.assertEqual(subject.find_text(32), "abcdefg")

    def test_get_text_from_member_array(self):
        array = ArraySingleString.fabricate(100, [
            BinaryObjectString.from_params(32, "abcdefg"), BinaryObjectString.from_params(27, "ﾈｺﾁｬﾝ")])

        subject = self.fabricate_with(500, [array])

        self.assertEqual(subject.find_text(27), "ﾈｺﾁｬﾝ")
        self.assertEqual(subject.find_text(32), "abcdefg")
        self.assertEqual(subject.has_bos_recursively(27), True)
        self.assertEqual(subject.has_bos_recursively(26), False)
        with self.assertRaises(Exception):
            subject.find_text(90)

    def test_get_text_recursively(self):
        """
        直下のオブジェクトが正しく実装されたget_text()メソッドを持っている前提
        """
        target = BinaryObjectString.from_params(27, "ﾈｺﾁｬﾝ")
        child_object = Mock(ClassWithValues)
        child_object.has_bos_recursively.return_value = True
        child_object.get_bos_recursively.return_value = target
        child_object.raw_bytes = b"mock_class_with_values"
        values = ValueArray([BinaryObjectString.from_params(1, "dummy"), child_object])

        record_header, class_info = self.fabricate_knickknacks()
        member_type_info = self.fabricate_mock_member_type_info(values)

        subject = ClassWithValues(record_header, class_info, member_type_info, [], values)
        self.assertEqual("ﾈｺﾁｬﾝ", subject.find_text(27))

    def test_replace_text_direct_child(self):
        inuchan = BinaryObjectString.from_params(56, "ｲﾇﾁｬﾝ")
        ojisan = BinaryObjectString.from_params(27, "ｵｼﾞｻﾝ")

        subject = self.fabricate_with(120, [inuchan, ojisan])

        subject.replace_text("ﾈｺﾁｬﾝ", 27)

        self.assertEqual(subject.find_text(27), "ﾈｺﾁｬﾝ")
        self.assertEqual(ojisan.get_string(), "ﾈｺﾁｬﾝ")
        self.assertEqual(inuchan.get_string(), "ｲﾇﾁｬﾝ")

    def test_replace_text_recursively(self):
        inuchan = BinaryObjectString.from_params(56, "ｲﾇﾁｬﾝ")
        ojisan = BinaryObjectString.from_params(27, "ｵｼﾞｻﾝ")
        cage = self.fabricate_with(555, [
            inuchan,
            ojisan
        ])
        assert cage.get_object_id() == 555

        subject = self.fabricate_with(1200, [cage])

        subject.replace_text("ﾈｺﾁｬﾝ", 27)

        self.assertEqual(subject.find_text(27), "ﾈｺﾁｬﾝ")
        self.assertEqual(ojisan.get_string(), "ﾈｺﾁｬﾝ")
        self.assertEqual(inuchan.get_string(), "ｲﾇﾁｬﾝ")

    def test_get_all_texts(self):
        # TODO: テスト　すべてのテキストのリスティング
        pass

    def test_has_valid_byte_array(self):
        # TODO: テスト　バイト列が正しく置換で保たれるか
        pass

if __name__ == '__main__':
    unittest.main()
