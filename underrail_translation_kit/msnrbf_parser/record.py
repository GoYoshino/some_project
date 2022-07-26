from typing import List

from .enums import RecordType
from .primitives import Int8
from .serialized_object import SerializedObject
from .serialized_object_array import SerializedObjectArray


class Record(SerializedObjectArray):

    def __init__(self, record_type: Int8, items: List[SerializedObject]):
        assert RecordType.has_value(record_type.value())

        self.record_type = RecordType(record_type.value())

        super().__init__([record_type] + items)