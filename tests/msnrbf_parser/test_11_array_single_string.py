import unittest
from typing import List

from underrail_translation_kit.msnrbf_parser.binary_object_string import BinaryObjectString
from underrail_translation_kit.msnrbf_parser.enums import RecordType
from underrail_translation_kit.msnrbf_parser.misc_record_classes import ArraySingleString, ObjectNullMultiple256
from underrail_translation_kit.msnrbf_parser.object_null import ObjectNull
from underrail_translation_kit.msnrbf_parser.primitives import Int8, RecordHeader
from underrail_translation_kit.msnrbf_parser.serialized_object import SerializedObject
from .helper import assertEndOfStream, assertEqualToStream


class ArraySingleStringTest(unittest.TestCase):

    def test_fabricate_with_texts(self):
        object_id = 500
        nekochan = BinaryObjectString.from_params(24, "ﾈｺﾁｬﾝ")
        inuchan = BinaryObjectString.from_params(18, "ｲﾇﾁｬﾝ")
        values = [
            BinaryObjectString.from_params(24, "ﾈｺﾁｬﾝ"),
            BinaryObjectString.from_params(18, "ｲﾇﾁｬﾝ"),
        ]

        subject = ArraySingleString.fabricate(object_id, values)

        expected_bytes = RecordHeader(RecordType.ArraySingleString).raw_bytes
        expected_bytes += object_id.to_bytes(4, "little")
        expected_bytes += len(values).to_bytes(4, "little")
        expected_bytes += nekochan.raw_bytes + inuchan.raw_bytes
        self.assertEqual(subject.raw_bytes, expected_bytes)

    def test_with_null(self):
        object_id = 500
        nekochan = BinaryObjectString.from_params(24, "ﾈｺﾁｬﾝ")
        inuchan = BinaryObjectString.from_params(18, "ｲﾇﾁｬﾝ")
        values = [
            ObjectNull(),
            BinaryObjectString.from_params(24, "ﾈｺﾁｬﾝ"),
            BinaryObjectString.from_params(18, "ｲﾇﾁｬﾝ"),
        ]

        subject = ArraySingleString.fabricate(object_id, values)

        expected_bytes = RecordHeader(RecordType.ArraySingleString).raw_bytes
        expected_bytes += object_id.to_bytes(4, "little")
        expected_bytes += len(values).to_bytes(4, "little")
        expected_bytes += ObjectNull().raw_bytes
        expected_bytes += nekochan.raw_bytes + inuchan.raw_bytes
        self.assertEqual(subject.raw_bytes, expected_bytes)

    def test_with_null_multiple(self):
        object_id = 500
        nekochan = BinaryObjectString.from_params(24, "ﾈｺﾁｬﾝ")
        inuchan = BinaryObjectString.from_params(18, "ｲﾇﾁｬﾝ")
        values = [
            BinaryObjectString.from_params(24, "ﾈｺﾁｬﾝ"),
            ObjectNullMultiple256.fabricate(4),
            BinaryObjectString.from_params(18, "ｲﾇﾁｬﾝ"),
        ]
        subject = ArraySingleString.fabricate(object_id, values)

        expected_bytes = RecordHeader(RecordType.ArraySingleString).raw_bytes
        expected_bytes += object_id.to_bytes(4, "little")
        expected_bytes += (6).to_bytes(4, "little")
        expected_bytes += nekochan.raw_bytes
        expected_bytes += ObjectNullMultiple256.fabricate(4).raw_bytes
        expected_bytes += inuchan.raw_bytes
        self.assertEqual(subject.raw_bytes, expected_bytes)

    def test_reading_stream(self):
        with open("msnrbf_parser/data/11_ArraySingleString", "rb") as stream:
            header = Int8.from_stream(stream)
            self.assertEqual(header.raw_bytes, b"\x11")
            obj = ArraySingleString.from_stream(stream)

            assertEndOfStream(self, stream)
            assertEqualToStream(self, obj.raw_bytes, stream)

    def test_get_object_id(self):
        subject = ArraySingleString.fabricate(500, [])
        self.assertEqual(subject.get_object_id(), 500)

    def find_text(self):
        object_id = 500
        values = [
            BinaryObjectString.from_params(24, "ﾈｺﾁｬﾝ"),
            ObjectNullMultiple256.fabricate(4),
            BinaryObjectString.from_params(18, "ｲﾇﾁｬﾝ"),
        ]
        subject = ArraySingleString.fabricate(object_id, values)

        self.assertEqual(subject.find_text(24), "ﾈｺﾁｬﾝ")
        self.assertEqual(subject.find_text(18), "ｲﾇﾁｬﾝ")
        self.assertIsNone(subject.find_text(35))

    def test_replace_text(self):
        object_id = 500
        nekochan = BinaryObjectString.from_params(24, "ﾈｺﾁｬﾝ")
        inuchan = BinaryObjectString.from_params(18, "ｲﾇﾁｬﾝ")
        values = [
            nekochan,
            ObjectNullMultiple256.fabricate(4),
            inuchan
        ]
        subject = ArraySingleString.fabricate(object_id, values)
        subject.replace_text("ｵｼﾞｻﾝ", 24)

        self.assertEqual(subject.find_text(24), "ｵｼﾞｻﾝ")
        self.assertEqual(subject.find_text(18), "ｲﾇﾁｬﾝ")

    def get_all_texts(self):
        pass

if __name__ == '__main__':
    unittest.main()
