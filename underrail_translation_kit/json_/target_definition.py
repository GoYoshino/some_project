from typing import List
import re
import json

class TargetDefinition:

    def __init__(self, target_path: str, description: str):
        self.target_path = target_path
        self.description = description

    def to_jsonizable_object(self):
        return {
            "target_path": self.target_path,
            "description": self.description
        }

TARGET_DEFINITION = {
    "items": [
        TargetDefinition("C00.I:N", "Item Name"),
        TargetDefinition("C00.I:D", "Item Description")
    ]
}

if __name__ == "__main__":
    TargetDefinition("aaa", "yey")
    print(json)