from __future__ import annotations
from serialize import ISerialize
import utility.logger as logger
import controller as ctrl


@logger.trace_class
class Layout(ISerialize):
    def __init__(self, **kwargs):
        self.name: str = kwargs.get("name", "Default")
        self.controllers: list[ctrl.Controller] = kwargs.get("controllers", [])

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "controllers": [controller.serialize() for controller in self.controllers]
        }

    def deserialize(self, dict: dict) -> Layout:
        self.name: str = dict["name"]
        self.controllers: list[ctrl.Controller] = [ctrl.Controller().deserialize(controller) for controller in dict["controllers"]]
        return self

    def get_controller(self, controller_name: str) -> ctrl.Controller | None:
        return next(iter(controller for controller in self.controllers if controller.name == controller_name), None)

    def add_controller(self, controller: ctrl.Controller):
        if controller not in self.controllers:
            self.controllers.append(controller)

    def replace_controller(self, old: ctrl.Controller, new: ctrl.Controller):
        if old in self.controllers:
            self.controllers[self.controllers.index(old)] = new

    def remove_controller(self, controller: ctrl.Controller):
        if controller in self.controllers:
            self.controllers.remove(controller)
