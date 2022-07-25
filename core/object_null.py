from io import BytesIO

from core.primitives import Int8
from core.record import Record

class ObjectNull(Record):
    """
    Refers to 0A: ObjectNull Record
    """

    def __init__(self):
        record_type = Int8.from_stream(BytesIO(b"\x0A"))
        super().__init__(record_type, [])
