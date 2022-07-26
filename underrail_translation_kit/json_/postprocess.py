from typing import List, Dict
import re

def __postprocess(json_object: Dict[str, str]) -> bool:
    """

    :param json_object:
    :return: False if the entry should be deleted
    """

    # avoid empty values
    if json_object["originalText"] == "":
        return False

    # avoid value: "English" entries spam
    if json_object["originalText"] == "English" or json_object["originalText"] == "Serbian":
        return False

    # avoid ".DM.DM:DN" and ".DM.DM:DD"
    if json_object["classInfo"][:9] == ".DM.DM:DN" or ["classInfo"][:9] == ".DM.DM:DD":
        return False

    # avoid elements suffixed with something like "(301db70e-7a5a-40db-a103-21e6927c1834)"
    if re.search(r"[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}", json_object["originalText"]):
        return False

    return True

def postprocess(json_objects: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return_list = []
    for json_object in json_objects:
        if (__postprocess(json_object)):
            return_list.append(json_object)

    return return_list