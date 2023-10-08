from __future__ import annotations
from serialize import ISerialize
import Utility.logger as logger


@logger.trace_class
class Variable(ISerialize):
    def __init__(self, **kwargs):
        self.name: str = kwargs.get("name", "Default")
        self.type: str = kwargs.get("type", "Trigger")
        self.direction: str = kwargs.get("direction", "Output")
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
