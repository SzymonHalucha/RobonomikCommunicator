from __future__ import annotations
from utils.serialize import ISerialize
from models.controller import Controller


class Layout(ISerialize):
    def __init__(self, **kwargs):
        self.name: str = kwargs.get("name", "Default")
        self.controllers: list[Controller] = kwargs.get("controllers", [])

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "controllers": [controller.serialize() for controller in self.controllers]
        }

    def deserialize(self, dict: dict) -> Layout:
        self.name = dict["name"]
        self.controllers = [Controller().deserialize(controller) for controller in dict["controllers"]]
        return self

    def get_controller(self, controller_name: str) -> Controller:
        return next(iter(controller for controller in self.controllers if controller.name == controller_name), None)

    def add_controller(self, controller: Controller):
        if controller not in self.controllers:
            self.controllers.append(controller)

    def replace_controller(self, old: Controller, new: Controller):
        if old in self.controllers:
            self.controllers[self.controllers.index(old)] = new

    def remove_controller(self, controller: Controller):
        if controller in self.controllers:
            self.controllers.remove(controller)
