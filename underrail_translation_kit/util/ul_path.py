from pathlib import Path
import os
from typing import Tuple

class UnderrailPath:

    def __init__(self, arg_path_str: str, underrail_root: str, json_root: str):
        """
        実データのパスあるいはjsonディレクトリのパスを渡す。（どっちを渡したいケースもあるため）
        どちらにせよ、"data"ディレクトリをルートとして認識する
        :param arg_path: 実データあるいはjsonディレクトリのパス
        """
        arg_path = Path(arg_path_str)
        arg_filename = arg_path.parts[-1:]
        self.__underrail_filename = self.__get_unsuffixed_filename(arg_filename[0])
        self.__relative_dir = self.__make_relative_dir(arg_path)
        self.__underrail_data_dir = Path(underrail_root)
        self.__json_data_dir = Path(json_root)

    def __get_unsuffixed_filename(self, arg_filename: str) -> str:
        if arg_filename[-5:] == ".json":    # given is json
            return arg_filename[:-5]
        else:
            return arg_filename

    def __make_relative_dir(self, path: Path) -> Path:
        index = self.__get_data_directory_index(path)
        return Path("/".join(path.parts[index:-1]))

    def __get_data_directory_index(self, path: Path):
        index = 0
        for i, part in enumerate(path.parts):
            if part == "data":
                return index
        raise Exception(f'パスにdataディレクトリが含まれていません: {path}')

    def json(self) -> str:
        """
        JSONの側のパスを返す
        :return: 文字列
        """
        return os.path.join(str(self.__json_data_dir), str(self.__relative_dir) , str(self.__underrail_filename) + ".json")

    def datafile(self) -> str:
        """
        underrail dataの側のパスを返す
        :return: 文字列
        """
        return os.path.join(str(self.__underrail_data_dir), str(self.__relative_dir), str(self.__underrail_filename))