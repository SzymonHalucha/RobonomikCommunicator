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

    def on_port_select(self, port: str):
        self.messenger.open(port, self.session.default_baudrate)

    def on_preset_create(self, name: str, callback: Callable[[bool], None]):
        if self.session.check_if_preset_name_is_valid(name):
            self.session.set_current_preset(Preset(name=name))
            self.session.save_session()
            callback(True)
        else:
            callback(False)

    def on_preset_select(self, callback: Callable[[None], None]) -> list[tuple[str, str, Callable[[str], None]]]:
        def on_select(content):
            self.session.set_current_preset(self.session.get_preset_by_id(content.id))
            callback(None)
        return [(preset.name, preset.id, on_select) for preset in self.session.get_presets().values()]

    def on_preset_delete(self):
        self.session.remove_current_preset()
        self.session.save_session()
