from __future__ import annotations
from datetime import datetime
from serialize import ISerialize
import utility.logger as logger
import variable as vrbl
import layout as lyot


@logger.trace_class
class Preset(ISerialize):
    def __init__(self, **kwargs):
        self.name: str = kwargs.get("name", "Default")
        self.ports: dict[str, float] = kwargs.get("ports", {})
        self.variables: list[vrbl.Variable] = kwargs.get("variables", [])
        self.layouts: list[lyot.Layout] = kwargs.get("layouts", [])
        self._current_layout: lyot.Layout = kwargs.get("current_layout", None)

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
        self.variables = [vrbl.Variable().deserialize(variable) for variable in dict["variables"]]
        self.layouts = [lyot.Layout().deserialize(layout) for layout in dict["layouts"]]
        self._current_layout = self.get_layout(dict["current_layout_name"])
        return self

    def get_port(self, port_name: str) -> float:
        return self.ports[port_name] if port_name in self.ports else 0

    def add_port(self, port_name: str):
        self.ports[port_name] = datetime.now().timestamp()

    def remove_port(self, port_name: str):
        self.ports.pop(port_name, None)

    def get_variable(self, variable_name: str) -> vrbl.Variable | None:
        return next(iter(variable for variable in self.variables if variable.name == variable_name), None)

    def add_variable(self, variable: vrbl.Variable):
        if variable not in self.variables:
            self.variables.append(variable)

    def replace_variable(self, old: vrbl.Variable, new: vrbl.Variable):
        if old in self.variables:
            self.variables[self.variables.index(old)] = new

    def remove_variable(self, variable: vrbl.Variable):
        if variable in self.variables:
            self.variables.remove(variable)

    def get_layout(self, layout_name: str) -> lyot.Layout | None:
        return next(iter(layout for layout in self.layouts if layout.name == layout_name), None)

    def add_layout(self, layout: lyot.Layout):
        if layout not in self.layouts:
            self.layouts.append(layout)

    def remove_layout(self, layout: lyot.Layout):
        if layout in self.layouts:
            self.layouts.remove(layout)

    def get_current_layout(self) -> lyot.Layout:
        return self._current_layout

    def set_current_layout(self, layout: lyot.Layout):
        if layout not in self.layouts:
            self.layouts.append(layout)
        self._current_layout = layout
