from typing import BinaryIO

def assertEndOfStream(test_class, stream: BinaryIO):
    test_class.assertEqual(stream.read(1), b"")

def assertEqualToStream(test_class, raw_bytes: bytes, stream: BinaryIO):
    stream.seek(0)
    expected_raw_bytes = stream.read()
    test_class.assertEqual(raw_bytes, expected_raw_bytes)