from io import BinaryIO

def assertEndOfStream(self, stream: BinaryIO):
    self.assertEqual(stream.read(1), b"\x0b")
    self.assertEqual(stream.read(1), b"")