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
        self.default_baudrate: int = 9600
        self.show_console_timestamps: bool = True
        self._presets: dict[str, Preset] = {}
        self._current_preset: str = ""
        self._messenger: Messenger = None
        self._saver: Saver = None

    def get_references(self):
        app = MDApp.get_running_app()
        self._saver: Saver = app.saver
        self._messenger: Messenger = app.messenger
        self._saver.register(self)

    def serialize(self) -> dict:
        return {
            "default_baudrate": self.default_baudrate,
            "show_console_timestamps": self.show_console_timestamps,
            "_presets": [preset.serialize() for preset in self._presets.values()],
            "_current_preset": self._current_preset
        }

    def deserialize(self, dict: dict) -> Session:
        self.default_baudrate = dict["default_baudrate"]
        self.show_console_timestamps = dict["show_console_timestamps"]
        self._presets = {preset["id"]: Preset().deserialize(preset) for preset in dict["_presets"]}
        self._current_preset = dict["_current_preset"]
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
        if len(self._presets) <= 0:
            preset = Preset()
            self._presets[preset.id] = preset
            self._current_preset = preset.id
        if self._current_preset == "" or self._current_preset not in self._presets:
            preset = next(iter(self._presets.values()))
            self._current_preset = preset.id
        if self._messenger is not None and self._messenger.is_open:
            preset: Preset = next(iter(sorted(self._presets.values(), key=lambda x: x.get_port(self._messenger.port), reverse=True)))
            preset.add_port(self._messenger.port)
            self._current_preset = preset.id
        return self._presets[self._current_preset]

    def set_current_preset(self, preset: Preset) -> Preset:
        if self._messenger is not None and self._messenger.is_open:
            preset.add_port(self._messenger.port)
        self._presets[preset.id] = preset
        self._current_preset = preset.id
        return preset

    def remove_current_preset(self):
        self._presets.pop(self._current_preset, None)
        self._current_preset = ""
        self.get_current_preset()

    def get_current_layout(self) -> Layout:
        return self.get_current_preset().get_current_layout()

    def set_current_layout(self, layout: Layout) -> Layout:
        self.get_current_preset().set_current_layout(layout)
        return layout

    def remove_current_layout(self):
        current: Preset = self.get_current_preset()
        current.remove_layout_by_id(current.get_current_layout().id)
        current.set_current_layout(next(iter(current.get_layouts().values())))

    def get_presets(self) -> dict[str, Preset]:
        return self._presets

    def get_preset_by_id(self, id: str) -> Preset:
        return self._presets[id]

    def get_variables(self) -> dict[str, Variable]:
        return self._presets[self._current_preset].get_variables()

    def get_variable_by_id(self, id: str) -> Variable:
        return self._presets[self._current_preset].get_variable_by_id(id)

    def add_variable(self, variable: Variable) -> Variable:
        self._presets[self._current_preset].add_variable(variable)
        return variable

    def remove_variable(self, variable: Variable) -> Variable:
        self._presets[self._current_preset].remove_variable_by_id(variable.id)
        return variable

    def get_layouts(self) -> dict[str, Layout]:
        return self._presets[self._current_preset].get_layouts()

    def get_layout_by_id(self, id: str) -> Layout:
        return self._presets[self._current_preset].get_layout_by_id(id)

    def add_layout(self, layout: Layout) -> Layout:
        self._presets[self._current_preset].add_layout(layout)
        return layout

    def remove_layout(self, layout: Layout) -> Layout:
        self._presets[self._current_preset].remove_layout_by_id(layout.id)
        return layout

    def get_controllers(self) -> dict[str, Controller]:
        return self.get_current_layout().get_controllers()

    def get_controller_by_id(self, id: str) -> Controller:
        return self.get_current_layout().get_controller_by_id(id)

    def add_controller(self, controller: Controller) -> Controller:
        self.get_current_layout().add_controller(controller)
        return controller

    def remove_controller(self, controller: Controller) -> Controller:
        self.get_current_layout().remove_controller_by_id(controller.id)
        return controller

    def does_preset_name_exist(self, name: str, ignore_presets: list[Preset] = []) -> bool:
        return any(prst.name == name and prst not in ignore_presets for prst in self.get_presets().values())

    def does_variable_name_exist(self, name: str, ignore_variables: list[Variable] = []) -> bool:
        return any(vrbl.name == name and vrbl not in ignore_variables for vrbl in self.get_variables().values())

    def does_layout_name_exist(self, name: str, ignore_layouts: list[Layout] = []) -> bool:
        return any(lyut.name == name and lyut not in ignore_layouts for lyut in self.get_layouts().values())

    def does_controller_name_exist(self, name: str, ignore_controllers: list[Controller] = []) -> bool:
        return any(ctrl.name == name and ctrl not in ignore_controllers for ctrl in self.get_controllers().values())

    def check_if_preset_name_is_valid(self, name: str, ignore_presets: list[Preset] = []) -> bool:
        if name.replace(" ", "") == "" or self.does_preset_name_exist(name, ignore_presets):
            return False
        return True

    def check_if_variable_name_is_valid(self, name: str, ignore_variables: list[Variable] = []) -> bool:
        if name.replace(" ", "") == "" or self.does_variable_name_exist(name, ignore_variables):
            return False
        return True

    def check_if_layout_name_is_valid(self, name: str, ignore_layouts: list[Layout] = []) -> bool:
        if name.replace(" ", "") == "" or self.does_layout_name_exist(name, ignore_layouts):
            return False
        return True

    def check_if_controller_name_is_valid(self, name: str, ignore_controllers: list[Controller] = []) -> bool:
        if name.replace(" ", "") == "" or self.does_controller_name_exist(name, ignore_controllers):
            return False
        return True
