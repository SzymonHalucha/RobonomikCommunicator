from serialize import ISerialize
import logger


@logger.trace_class
class Controller(ISerialize):
    def __init__(self, **kwargs):
        self.name: "str" = kwargs.get("name", "Default")
        self.type: "str" = kwargs.get("type", Controller.get_types()[0])
        self.custom_name: "str" = kwargs.get("custom_name", "Default")
        self.variable_name: "str" = kwargs.get("variable_name", "Default")
        self.start_range: "str" = kwargs.get("start_range", "0")
        self.end_range: "str" = kwargs.get("end_range", "255")
        self.position: "tuple[float, float]" = kwargs.get("position", (0.5, 0.5))
        self.size: "tuple[int, int]" = kwargs.get("size", (200, 200))

    def serialize(self) -> "dict":
        return {
            "name": self.name,
            "type": self.type,
            "custom_name": self.custom_name,
            "variable_name": self.variable_name,
            "start_range": self.start_range,
            "end_range": self.end_range,
            "position": self.position,
            "size": self.size
        }

    def deserialize(self, dict: "dict") -> "Controller":
        self.name = dict["name"]
        self.type = dict["type"]
        self.custom_name = dict["custom_name"]
        self.variable_name = dict["variable_name"]
        self.start_range = dict["start_range"]
        self.end_range = dict["end_range"]
        self.position = dict["position"]
        self.size = dict["size"]
        return self

    @classmethod
    def get_types(cls) -> "tuple[str, ...]":
        return ("Trigger", "Switch", "Slider", "Input")
