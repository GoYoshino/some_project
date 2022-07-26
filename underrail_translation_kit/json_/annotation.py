from typing import Dict

def __add_annotation(json_dict: Dict[str, str], path_to_target: str, annotation: str):
    if json_dict["targetPath"] == path_to_target:
        json_dict["description"] = annotation

def add_annotation(json_dict: Dict[str, str]) -> None:

    __add_annotation(json_dict, "C00.I:N", "Item name")
    __add_annotation(json_dict, "C00.I:D", "Item description")