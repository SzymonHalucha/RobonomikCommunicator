from __future__ import annotations
from utils.serialize import ISerialize
from models.variable import Variable
from models.layout import Layout
from datetime import datetime
import uuid


class Preset(ISerialize):
    def __init__(self, **kwargs):
        self.id: str = uuid.uuid4().hex
        self.name: str = kwargs.get("name", "Default")
        self._ports: dict[str, float] = kwargs.get("ports", {})
        self._variables: dict[str, Variable] = kwargs.get("variables", {})
        self._layouts: dict[str, Layout] = kwargs.get("layouts", {})
        self._current_layout: str = kwargs.get("current_layout", "")

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "_ports": self._ports,
            "_variables": [variable.serialize() for variable in self._variables.values()],
            "_layouts": [layout.serialize() for layout in self._layouts.values()],
            "_current_layout": self._current_layout
        }

    def deserialize(self, dict: dict) -> Preset:
        self.id = dict["id"]
        self.name = dict["name"]
        self._ports = dict["_ports"]
        self._variables = {variable["id"]: Variable().deserialize(variable) for variable in dict["_variables"]}
        self._layouts = {layout["id"]: Layout().deserialize(layout) for layout in dict["_layouts"]}
        self._current_layout = dict["_current_layout"]
        return self

    def get_ports(self) -> dict[str, float]:
        return self._ports

    def get_port(self, port_name: str) -> float:
        return self._ports[port_name] if port_name in self._ports else 0

    def add_port(self, port_name: str):
        self._ports[port_name] = datetime.now().timestamp()

    def remove_port(self, port_name: str):
        self._ports.pop(port_name, None)

    def get_variables(self) -> dict[str, Variable]:
        return self._variables

    def get_variable_by_id(self, id: str) -> Variable:
        return self._variables[id]

    def add_variable(self, variable: Variable):
        self._variables[variable.id] = variable

    def remove_variable_by_id(self, id: str):
        if id in self._variables:
            self._variables.pop(id, None)

    def get_layouts(self) -> dict[str, Layout]:
        return self._layouts

    def get_layout_by_id(self, id: str) -> Layout:
        return self._layouts[id]

    def get_current_layout(self) -> Layout:
        if self._current_layout == "" or len(self._layouts) <= 0:
            self.set_current_layout(Layout())
        elif self._current_layout not in self._layouts:
            self._current_layout = next(iter(self._layouts.values())).id
        return self._layouts[self._current_layout]

    def set_current_layout(self, layout: Layout):
        self._layouts[layout.id] = layout
        self._current_layout = layout.id

    def add_layout(self, layout: Layout):
        self._layouts[layout.id] = layout

    def remove_layout_by_id(self, id: str):
        if id in self._layouts:
            self._layouts.pop(id, None)
