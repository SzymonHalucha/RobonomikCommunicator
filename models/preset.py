from __future__ import annotations
from utils.serialize import ISerialize
from models.variable import Variable
from models.layout import Layout
from datetime import datetime


class Preset(ISerialize):
    def __init__(self, **kwargs):
        self.name: str = kwargs.get("name", "Default")
        self.ports: dict[str, float] = kwargs.get("ports", {})
        self.variables: list[Variable] = kwargs.get("variables", [])
        self.layouts: list[Layout] = kwargs.get("layouts", [])
        self._current_layout: Layout = kwargs.get("current_layout", None)

    def serialize(self) -> dict:
        return {
            "name": self.name,
            "ports": self.ports,
            "variables": [variable.serialize() for variable in self.variables],
            "layouts": [layout.serialize() for layout in self.layouts],
            "current_layout_name": self._current_layout.name if self._current_layout is not None else None
        }

    def deserialize(self, dict: dict) -> Preset:
        self.name = dict["name"]
        self.ports = dict["ports"]
        self.variables = [Variable().deserialize(variable) for variable in dict["variables"]]
        self.layouts = [Layout().deserialize(layout) for layout in dict["layouts"]]
        self._current_layout = self.get_layout(dict["current_layout_name"])
        return self

    def get_port(self, port_name: str) -> float:
        return self.ports[port_name] if port_name in self.ports else 0

    def add_port(self, port_name: str):
        self.ports[port_name] = datetime.now().timestamp()

    def remove_port(self, port_name: str):
        self.ports.pop(port_name, None)

    def get_variable(self, variable_name: str) -> Variable:
        return next(iter(variable for variable in self.variables if variable.name == variable_name), None)

    def add_variable(self, variable: Variable):
        if variable not in self.variables:
            self.variables.append(variable)

    def replace_variable(self, old: Variable, new: Variable):
        if old in self.variables:
            self.variables[self.variables.index(old)] = new

    def remove_variable(self, variable: Variable):
        if variable in self.variables:
            self.variables.remove(variable)

    def get_layout(self, layout_name: str) -> Layout:
        return next(iter(layout for layout in self.layouts if layout.name == layout_name), None)

    def get_current_layout(self) -> Layout:
        return self._current_layout

    def set_current_layout(self, layout: Layout):
        if layout not in self.layouts:
            self.layouts.append(layout)
        self._current_layout = layout

    def add_layout(self, layout: Layout):
        if layout not in self.layouts:
            self.layouts.append(layout)

    def remove_layout(self, layout: Layout):
        if layout in self.layouts:
            self.layouts.remove(layout)
