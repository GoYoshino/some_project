import gzip

def to_underrail_gzip(raw_bytes: bytes, header: bytes):
    """
    バイト列をunderrail準拠のgzipファイル(.item, .k)に圧縮する。
    24バイトのヘッダは別途用意する必要がある。
    :param raw_bytes: オブジェクトのバイト列(MS-NRBF)
    :param header: ヘッダ。24バイト。オリジナルファイルと同じものを用いることを参照
    :return: gzip圧縮されたバイト列
    """
    assert len(header) == 24
    compressed_bytes = header + gzip.compress(raw_bytes)
    return compressed_bytes