from __future__ import annotations
from utils.serialize import ISerialize
from models.controller import Controller
import uuid


class Layout(ISerialize):
    def __init__(self, **kwargs):
        self.id: str = uuid.uuid4().hex
        self.name: str = kwargs.get("name", "Default")
        self.controllers: dict[str, Controller] = kwargs.get("controllers", {})

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "controllers": [controller.serialize() for controller in self.controllers.values()]
        }

    def deserialize(self, dict: dict) -> Layout:
        self.id = dict["id"]
        self.name = dict["name"]
        self.controllers = {controller["id"]: Controller().deserialize(controller) for controller in dict["controllers"]}
        return self

    def get_controllers(self) -> dict[str, Controller]:
        return self.controllers

    def get_controller_by_id(self, id: str) -> Controller:
        return self.controllers[id]

    def add_controller(self, controller: Controller):
        self.controllers[controller.id] = controller

    def remove_controller_by_id(self, id: str):
        if id in self.controllers:
            self.controllers.pop(id, None)
