import gzip
from io import BytesIO

from decode import decode





def pack(raw_bytes: bytes) -> bytes:
    return MAGIC_HEADER + raw_bytes

if __name__ == "__main__":
    FILE = r"legacy\data\knowledge\items\ammo.k"

    raw_bytes = unpack(FILE)
    decode(BytesIO(raw_bytes))