from serialize import ISerialize
import logger


@logger.trace_class
class Variable(ISerialize):
    def __init__(self, **kwargs):
        self.name: "str" = kwargs.get("name", "Default")
        self.type: "str" = kwargs.get("type", Variable.get_types()[0])
        self.direction: "str" = kwargs.get("direction", Variable.get_directions()[0])
        self.interval: "int" = kwargs.get("interval", 100)

    def serialize(self) -> "dict":
        return {
            "name": self.name,
            "type": self.type,
            "direction": self.direction,
            "interval": self.interval
        }

    def deserialize(self, dict: "dict") -> "Variable":
        self.name = dict["name"]
        self.type = dict["type"]
        self.direction = dict["direction"]
        self.interval = dict["interval"]
        return self

    @classmethod
    def get_types(cls) -> "tuple[str, ...]":
        return ("Int", "Float", "String")

    @classmethod
    def get_directions(cls) -> "tuple[str, ...]":
        return ("Output", "Input")
