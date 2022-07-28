from .primitives import RecordHeader, Int32
from .record import Record
from .serialized_object_array import SerializedObjectArray


class ClassWithID(Record):
    """
        Refers to 01: ClassWithID Record
        Does not care detailed behavior as long as the instance preserves original raw byte array
        Because header has nothing to do with translation work
        """

    def __init__(self, record_header: RecordHeader, object_id: Int32, metadata_id: Int32, values: SerializedObjectArray, meta_class_info):
        super().__init__(record_header, [object_id, metadata_id, values])
        self.__meta_class_info = meta_class_info

    def __repr__(self):
        return "ClassWithID"