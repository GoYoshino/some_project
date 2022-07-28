from pathlib import Path
import os
from typing import Tuple

class UnderrailPath:

    def __init__(self, arg_path_str: str, underrail_root: str, json_root: str, patch_root: str=None):
        """
        まとめてファイルの書き換えやjsonの生成を行う際に便利なパスの変換を行う
        "data"ディレクトリをルートとして認識する
        :param arg_path_str: 実データのパスあるいはjsonディレクトリのパスを渡す。（どっちを渡したいケースもあるため）
        :param underrail_root: underrailのdataディレクトリのパス
        :param json_root: jsonのdataディレクトリのパス
        :param patch_root: (Optional) パッチ保存先のdataディレクトリのパス
        """

        arg_path = Path(arg_path_str)
        arg_filename = arg_path.parts[-1:]
        self.__unsuffixed_filename = self.__get_unsuffixed_filename(arg_filename[0])
        self.__relative_dir = self.__make_relative_dir(arg_path)

        self.__underrail_data_root = Path(underrail_root)
        self.__json_root = Path(json_root)
        self.__patch_root = None if patch_root is None else Path(patch_root)

    def __get_unsuffixed_filename(self, arg_filename: str) -> str:
        if arg_filename[-5:] == ".json":    # given is json
            return arg_filename[:-5]
        else:
            return arg_filename

    def __make_relative_dir(self, path: Path) -> Path:
        index = self.__get_data_directory_index(path)
        return Path(os.sep.join(path.parts[index + 1:-1]))

    def __get_data_directory_index(self, path: Path):
        for i, part in enumerate(path.parts):
            if part == "data":
                return i
        raise Exception(f'パスにdataディレクトリが含まれていません: {path}')

    def json(self) -> str:
        """
        JSONの側のパスを返す
        :return: 文字列
        """
        return os.path.join(str(self.__json_root), str(self.__relative_dir), str(self.__unsuffixed_filename) + ".json")

    def datafile(self) -> str:
        """
        underrail dataの側のパスを返す
        :return: 文字列
        """
        return os.path.join(str(self.__underrail_data_root), str(self.__relative_dir), str(self.__unsuffixed_filename))

    def patch(self):
        """
        patch出力先のパスを返す
        :return: 文字列
        """
        if self.__patch_root is None:
            raise Exception("patch data dirが登録されていません")
        return os.path.join(str(self.__patch_root), str(self.__relative_dir), str(self.__unsuffixed_filename))

    def json_dir(self) -> str:
        return os.path.join(str(self.__json_root), str(self.__relative_dir))

    def datafile_dir(self) -> str:
        return os.path.join(str(self.__underrail_data_root), str(self.__relative_dir))

    def patch_dir(self):
        if self.__patch_root is None:
            raise Exception("patch data dirが登録されていません")
        return os.path.join(str(self.__patch_root), str(self.__relative_dir))