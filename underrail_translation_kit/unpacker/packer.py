import gzip

def to_underrail_gzip(raw_bytes: bytes, header: bytes):
    assert len(header) == 24
    compressed_bytes = header + gzip.compress(raw_bytes)
    return compressed_bytes