from io import BytesIO
from typing import BinaryIO
import gzip

def unpack_as_stream(filename: str) -> BinaryIO:
    byte_array = unpack(filename)
    return BytesIO(byte_array)

def unpack(filename: str) -> bytes:
    with open(filename, "rb") as f:
        f.seek(24)
        return gzip.GzipFile(fileobj=f, mode="rb").read()