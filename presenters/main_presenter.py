from __future__ import annotations
from typing import Callable
from presenters.base_presenter import BasePresenter
from models.messenger import Messenger
from models.session import Session
from models.preset import Preset
import serial.tools.list_ports


class MainPresenter(BasePresenter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messenger: Messenger = kwargs.get("messenger", None)
        self.session: Session = kwargs.get("session", None)

    def get_dict_of_settings(self) -> dict:
        return {
            "preset_name": self.session.get_current_preset().name,
            "default_baudrate": self.session.default_baudrate,
            "show_console_timestamps": self.session.show_console_timestamps
        }

    def on_settings_changed(self, key: str, value):
        self.session.set_param(key, value)

    def on_ports_list_refresh(self, callback: Callable[[list[tuple[str, str]]], None]) -> list[tuple[str, str]]:
        ports = [(port.device, port.description) for port in serial.tools.list_ports.comports()]
        if callback is not None:
            callback(ports)
        return ports

    def on_port_select(self, port: str, callback: Callable[[None], None]):
        self.messenger.open(port, self.session.default_baudrate)
        callback(None)

    def on_preset_create(self, name: str, callback: Callable[[bool], None]):
        preset = Preset(name=name)
        if self.session.check_if_preset_is_valid(preset):
            self.session.set_current_preset(preset)
            self.session.save_session()
            callback(True)
        else:
            callback(False)

    def on_preset_select(self, callback: Callable[[None], None]) -> list[tuple[str, Callable[[str], None]]]:
        def on_select(name: str):
            self.session.set_current_preset(self.session.get_preset_by_name(name))
            callback(None)
        return [(preset.name, on_select) for preset in self.session.get_presets()]

    def on_preset_delete(self, callback: Callable[[None], None]):
        self.session.remove_current_preset()
        self.session.save_session()
        callback(None)
