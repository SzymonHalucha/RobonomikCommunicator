from __future__ import annotations
from utils.serialize import ISerialize


class Variable(ISerialize):
    def __init__(self, **kwargs):
        self.name: str = kwargs.get("name", "Default")
        self.type: str = kwargs.get("type", Variable.get_type()[0])
        self.direction: str = kwargs.get("direction", Variable.get_direction()[0])
        self.interval: int = kwargs.get("interval", 100)

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "direction": self.direction,
            "interval": self.interval
        }

    def deserialize(self, dict: dict) -> Variable:
        self.name = dict["name"]
        self.type = dict["type"]
        self.direction = dict["direction"]
        self.interval = dict["interval"]
        return self

    @staticmethod
    def get_type() -> tuple[str, ...]:
        return ("Int", "Float", "String")

    @staticmethod
    def get_direction() -> tuple[str, ...]:
        return ("Output", "Input")
