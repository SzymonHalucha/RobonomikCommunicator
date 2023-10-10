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

    def on_settings_update(self, *args):
        self.session.set_param(args[0], args[1])

    def on_ports_list_refresh(self, callback: Callable[[list[str, str]], None] = None) -> list[str, str]:
        ports = [(port.device, port.description) for port in serial.tools.list_ports.comports()]
        if callback is not None:
            callback(ports)
        return ports

    def on_port_select(self, port: str, callback: Callable[[None], None] = None):
        self.messenger.open(port, self.session.default_baudrate)
        if callback is not None:
            callback()

    def on_preset_create(self, name: str, callback: Callable[[bool], None] = None):
        preset = Preset(name=name)
        if self.session.check_if_preset_is_valid(preset):
            self.session.set_current_preset(preset)
            self.session.save_session()
            if callback is not None:
                callback(True)
        else:
            if callback is not None:
                callback(False)

    def on_preset_select(self, callback: Callable[[None], None] = None) -> list[tuple[str, Callable[[str], None]]]:
        def on_select(name: str):
            self.session.set_current_preset(self.session.get_preset_by_name(name))
            if callback is not None:
                callback()
        return [(preset.name, on_select) for preset in self.session.get_presets()]

    def on_preset_delete(self, callback: Callable[[None], None] = None):
        self.session.remove_current_preset()
        self.session.save_session()
        if callback is not None:
            callback()
