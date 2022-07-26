from typing import List

from .enums import RecordType
from .primitives import RecordHeader
from .serialized_object import SerializedObject
from .serialized_object_array import SerializedObjectArray


class Record(SerializedObjectArray):

    def __init__(self, record_header: RecordHeader, items: List[SerializedObject]):
        self.record_type = record_header.record_type

        super().__init__([record_header] + items)