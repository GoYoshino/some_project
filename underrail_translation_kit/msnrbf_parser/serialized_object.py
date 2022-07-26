class SerializedObject:
    """
    シリアライズされたオブジェクトの基本クラス
    """

    def __init__(self, raw_bytes: bytes):
        self.raw_bytes = raw_bytes

    def recalc_raw_bytes(self):
        pass