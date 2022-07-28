from io import BytesIO
from typing import BinaryIO

from .util import AltGzipFile

def unpack_as_stream(filepath: str) -> BinaryIO:
    """
    指定されたunderrailファイルを読み込み、MS-NRBFとして読み込めるバイト列をストリームとして返す。
    :param filepath: ファイルパス
    :return: バイト列、MS-NRBF準拠
    """
    byte_array = unpack(filepath)
    return BytesIO(byte_array)

def unpack(filename: str) -> bytes:
    """
    指定されたunderrailファイルを読み込み、MS-NRBFとして読み込めるバイト列を返す。
    :param filepath: ファイルパス
    :return: バイト列、MS-NRBF準拠
    """

    with open(filename, "rb") as f:
        f.seek(24)
        gzip_magic = f.read(2)
        f.seek(f.tell() - 2)
        if gzip_magic == b"\x1F\x8B":
            return AltGzipFile(fileobj=f, mode="rb").read()
        else:
            return f.read()