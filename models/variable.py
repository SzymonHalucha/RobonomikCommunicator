from __future__ import annotations
from utils.serialize import ISerialize
import uuid


class Variable(ISerialize):
    def __init__(self, **kwargs):
        self.id: str = uuid.uuid4().hex
        self.name: str = kwargs.get("name", "Default")
        self.type: str = kwargs.get("type", Variable.get_type()[0])
        self.direction: str = kwargs.get("direction", Variable.get_direction()[0])
        self.interval: int = kwargs.get("interval", 100)

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "direction": self.direction,
            "interval": self.interval
        }

    def deserialize(self, dict: dict) -> Variable:
        self.id = dict["id"]
        self.name = dict["name"]
        self.type = dict["type"]
        self.direction = dict["direction"]
        self.interval = dict["interval"]
        return self

    def copy_from_dict(self, dict: dict):
        self.name = dict["name"]
        self.type = dict["type"]
        self.direction = dict["direction"]
        self.interval = dict["interval"]

    @staticmethod
    def get_type() -> tuple[str, ...]:
        return ("Int", "Float", "String")

    @staticmethod
    def get_direction() -> tuple[str, ...]:
        return ("Output", "Input")
