from __future__ import annotations
from kivymd.app import MDApp
from utils.serialize import ISerialize
from models.controller import Controller
from models.messenger import Messenger
from models.variable import Variable
from models.preset import Preset
from models.layout import Layout
from models.saver import Saver


class Session(ISerialize):
    def __init__(self):
        self._presets: list[Preset] = []
        self.default_baudrate: int = 9600
        self.show_console_timestamps: bool = True
        self._current_preset: Preset = None
        self._messenger: Messenger = None
        self._saver: Saver = None

    def get_references(self):
        app = MDApp.get_running_app()
        self._saver: Saver = app.saver
        self._messenger: Messenger = app.messenger
        self._saver.register(self)

    def serialize(self) -> dict:
        return {
            "presets": [preset.serialize() for preset in self._presets],
            "current_preset_name": self._current_preset.name if self._current_preset is not None else None,
            "default_baudrate": self.default_baudrate,
            "show_console_timestamps": self.show_console_timestamps
        }

    def deserialize(self, dict: dict) -> Session:
        self._presets = [Preset().deserialize(preset) for preset in dict["presets"]]
        self._current_preset = self.get_preset_by_name(dict["current_preset_name"])
        self.default_baudrate = dict["default_baudrate"]
        self.show_console_timestamps = dict["show_console_timestamps"]
        return self

    def get_param(self, param: str):
        return getattr(self, param, None)

    def set_param(self, param: str, value):
        if hasattr(self, param):
            setattr(self, param, value)
            self.save_session()

    def save_session(self):
        self._saver.save_config()

    def discard_session(self):
        self._saver.load_config()
        self._saver.register(self)

    def get_current_preset(self) -> Preset:
        preset = self._current_preset
        if preset is None and len(self._presets) <= 0:
            preset = Preset()
            preset = self._presets.append(preset)
        if self._messenger is not None and self._messenger.is_open:
            preset = next(iter(sorted(self._presets, key=lambda x: x.get_port(self._messenger.port), reverse=True)), None)
            preset.add_port(self._messenger.port)
        if preset is None:
            preset = self._presets[0]
        self._current_preset = preset
        return preset

    def set_current_preset(self, preset: Preset) -> Preset:
        if self._messenger is not None and self._messenger.is_open:
            preset.add_port(self._messenger.port)
        if preset not in self._presets:
            self._presets.append(preset)
        self._current_preset = preset
        return preset

    def remove_current_preset(self):
        if self._current_preset in self._presets:
            self._presets.remove(self._current_preset)
        self._current_preset = None
        self.get_current_preset()

    def get_current_layout(self) -> Layout:
        if self._current_preset.get_current_layout() is None and len(self._current_preset.layouts) <= 0:
            self._current_preset.set_current_layout(Layout())
        elif self._current_preset.get_current_layout() is None:
            self._current_preset.set_current_layout(self._current_preset.layouts[0])
        return self._current_preset.get_current_layout()

    def set_current_layout(self, layout: Layout) -> Layout:
        self._current_preset.set_current_layout(layout)
        return layout

    def remove_current_layout(self):
        self._current_preset.remove_layout(self._current_preset.get_current_layout())
        self._current_preset.set_current_layout(self._current_preset.layouts[0])

    def get_presets(self) -> list[Preset]:
        return self._presets

    def get_preset_by_name(self, name: str) -> Preset:
        return next(iter(preset for preset in self._presets if preset.name == name), None)

    def get_variables(self) -> list[Variable]:
        return self._current_preset.variables

    def get_variable_by_name(self, name: str) -> Variable:
        return self._current_preset.get_variable(name)

    def add_variable(self, variable: Variable) -> Variable:
        self._current_preset.variables.append(variable)
        return variable

    def replace_variable(self, old: Variable, new: Variable) -> Variable:
        self._current_preset.replace_variable(old, new)
        return new

    def remove_variable(self, variable: Variable) -> Variable:
        self._current_preset.remove_variable(variable)
        return variable

    def get_layouts(self) -> list[Layout]:
        return self._current_preset.layouts

    def get_layout_by_name(self, name: str) -> Layout:
        return self._current_preset.get_layout(name)

    def add_layout(self, layout: Layout) -> Layout:
        self._current_preset.layouts.append(layout)
        return layout

    def remove_layout(self, layout: Layout) -> Layout:
        self._current_preset.remove_layout(layout)
        return layout

    def get_controllers(self) -> list[Controller]:
        return self.get_current_layout().controllers

    def get_controller_by_name(self, name: str) -> Controller:
        return self.get_current_layout().get_controller(name)

    def add_controller(self, controller: Controller) -> Controller:
        self.get_current_layout().add_controller(controller)
        return controller

    def replace_controller(self, old: Controller, new: Controller, copy_position: bool = True) -> Controller:
        if copy_position:
            new.position = old.position
        self.get_current_layout().replace_controller(old, new)
        return new

    def remove_controller(self, controller: Controller) -> Controller:
        self.get_current_layout().remove_controller(controller)
        return controller

    def does_preset_exist(self, preset: Preset, ignore_presets: list[Preset] = []) -> bool:
        return any(prst.name == preset.name and prst not in ignore_presets for prst in self._presets)

    def does_variable_exist(self, variable: Variable, ignore_variables: list[Variable] = []) -> bool:
        return any(vrbl.name == variable.name and vrbl not in ignore_variables for vrbl in self.get_current_preset().variables)

    def does_layout_exist(self, layout: Layout, ignore_layouts: list[Layout] = []) -> bool:
        return any(lyut.name == layout.name and lyut not in ignore_layouts for lyut in self.get_current_preset().layouts)

    def does_controller_exist(self, controller: Controller, ignore_controllers: list[Controller] = []) -> bool:
        return any(ctrl.name == controller.name and ctrl not in ignore_controllers for ctrl in self.get_controllers())

    def check_if_preset_is_valid(self, preset: Preset, ignore_presets: list[Preset] = []) -> bool:
        if preset.name.replace(" ", "") == "" or self.does_preset_exist(preset, ignore_presets):
            return False
        return True

    def check_if_variable_is_valid(self, variable: Variable, ignore_variables: list[Variable] = []) -> bool:
        if variable.name.replace(" ", "") == "" or self.does_variable_exist(variable, ignore_variables):
            return False
        return True

    def check_if_layout_is_valid(self, layout: Layout, ignore_layouts: list[Layout] = []) -> bool:
        if layout.name.replace(" ", "") == "" or self.does_layout_exist(layout, ignore_layouts):
            return False
        return True

    def check_if_controller_is_valid(self, controller: Controller, ignore_controllers: list[Controller] = []) -> bool:
        if controller.name.replace(" ", "") == "" or self.does_controller_exist(controller, ignore_controllers):
            return False
        return True
