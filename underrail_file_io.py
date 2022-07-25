import gzip
from io import BytesIO

from decode import decode

MAGIC_HEADER = b"\xF9\x53\x8B\x83\x1F\x36\x32\x43\xBA\xAE\x0D\x17\x86\x5D\x08\x54\xBA\x81\x7C\x81\x4A\x00\x00\x00"

def unpack(filename: str) -> bytes:
    with open(filename, "rb") as f:
        f.seek(24)
        return gzip.GzipFile(fileobj=f, mode="rb").read()

def pack(raw_bytes: bytes) -> bytes:
    return MAGIC_HEADER + raw_bytes

if __name__ == "__main__":
    FILE = r"legacy\data\knowledge\items\ammo.k"

    raw_bytes = unpack(FILE)
    decode(BytesIO(raw_bytes))