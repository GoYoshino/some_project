import gzip

MAGIC_HEADER = b"\xF9\x53\x8B\x83\x1F\x36\x32\x43\xBA\xAE\x0D\x17\x86\x5D\x08\x54\xBA\x81\x7C\x81\x4A\x00\x00\x00"

def to_underrail_gzip(raw_bytes: bytes):
    compressed_bytes = gzip.compress(raw_bytes)
    return MAGIC_HEADER + compressed_bytes