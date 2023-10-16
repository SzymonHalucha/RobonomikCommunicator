from __future__ import annotations
from utils.serialize import ISerialize
import uuid


class Controller(ISerialize):
    def __init__(self, **kwargs):
        self.id: str = uuid.uuid4().hex
        self.name: str = kwargs.get("name", "Default")
        self.type: str = kwargs.get("type", Controller.get_type()[0])
        self.custom_name: str = kwargs.get("custom_name", "Default")
        self.variable_name: str = kwargs.get("variable_name", "Default")
        self.range: tuple[float, float] = kwargs.get("range", (0, 100))
        self.position: tuple[float, float] = kwargs.get("position", (0.5, 0.5))
        self.size: tuple[int, int] = kwargs.get("size", (200, 200))

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "custom_name": self.custom_name,
            "variable_name": self.variable_name,
            "range": self.range,
            "position": self.position,
            "size": self.size
        }

    def deserialize(self, dict: dict) -> Controller:
        self.id = dict["id"]
        self.name = dict["name"]
        self.type = dict["type"]
        self.custom_name = dict["custom_name"]
        self.variable_name = dict["variable_name"]
        self.range = dict["range"]
        self.position = dict["position"]
        self.size = dict["size"]
        return self

    def copy_from_dict(self, dict: dict):
        self.name = dict["name"]
        self.type = dict["type"]
        self.custom_name = dict["custom_name"]
        self.variable_name = dict["variable_name"]
        self.range = dict["range"]
        self.size = dict["size"]

    @staticmethod
    def get_type() -> tuple[str, ...]:
        return ("Button", "Switch", "Slider", "Text Input")

    @staticmethod
    def get_direction() -> tuple[str, ...]:
        return ("Output", "Input")
