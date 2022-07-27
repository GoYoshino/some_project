from io import BytesIO
from typing import BinaryIO

from .util import AltGzipFile

def unpack_as_stream(filename: str) -> BinaryIO:
    byte_array = unpack(filename)
    return BytesIO(byte_array)

def unpack(filename: str) -> bytes:
    with open(filename, "rb") as f:
        f.seek(24)
        gzip_magic = f.read(2)
        if gzip_magic == b"\x1F\x8B":
            f.seek(f.tell() - 2)
            return AltGzipFile(fileobj=f, mode="rb").read()
        else:
            f.seek(f.tell() - 2)
            return f.read()