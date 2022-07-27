from .enums import RecordType
from .primitives import RecordHeader
from .record import Record

class ObjectNull(Record):
    """
    Refers to 0A: ObjectNull Record
    """

    def __init__(self):
        record_type = RecordHeader(RecordType.ObjectNull)
        super().__init__(record_type, [])