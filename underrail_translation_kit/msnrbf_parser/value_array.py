from typing import List

from .serialized_object import SerializedObject
from .serialized_object_array import SerializedObjectArray


class ValueArray(SerializedObjectArray):

    def __init__(self, items: List[SerializedObject]):
        super().__init__(items)