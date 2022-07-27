from typing import List, Dict
import re

def __postprocess(json_object: Dict[str, str]) -> bool:
    """

    :param json_object:
    :return: False if the entry should be deleted
    """

    # 1. avoid { className: "DM", value: "English" entries
    if json_object["className"] == "DM" and json_object["originalText"] == "English":
        return False

    # 2. avoid elements suffixed with something like "(301db70e-7a5a-40db-a103-21e6927c1834)"
    if re.search(r"[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}", json_object["originalText"]):
        return False

    # 3. give annotations for item
    if json_object["className"] == "I:N":
        json_object["description"] = "Item Name"
    elif json_object["className"] == "I:D":
        json_object["description"] = "Item Description"

    return True

def postprocess(json_objects: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return_list = []
    for json_object in json_objects:
        if (__postprocess(json_object)):
            return_list.append(json_object)

    return return_list