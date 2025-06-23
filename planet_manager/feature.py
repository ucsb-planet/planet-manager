from dataclasses import dataclass
from datetime import datetime

from dateutil.parser import parse

@dataclass
class Feature:
    type: str
    id: str
    properties: dict

    @staticmethod
    def load(input: dict):
        return Feature(
            input["type"],
            input["id"],
            input["properties"],
        )
