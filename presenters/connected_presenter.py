from __future__ import annotations
from typing import Callable
from presenters.base_presenter import BasePresenter
from models.variable import Variable
from models.controller import Controller
from models.layout import Layout
from models.messenger import Messenger
from models.session import Session


class ConnectedPresenter(BasePresenter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messenger: Messenger = kwargs.get("messenger", None)
        self.session: Session = kwargs.get("session", None)

    def on_close_port(self):
        self.session.save_session()
        self.messenger.close()

    def on_message_send(self, text: str, callback: Callable[[list[tuple[str, str, bool]], bool], None]):
        if text == "":
            return
        self.messenger.send(text)
        callback(self.messenger.history[-150:], self.session.show_console_timestamps)

    def get_messages_history(self) -> tuple[list[tuple[str, str, bool]], bool]:
        return (self.messenger.history[-150:], self.session.show_console_timestamps)

    def listen_for_messages_from_serial(self, callback: Callable):
        self.messenger.subscribe(callback)

    def stop_listen_for_messages_from_serial(self, callback: Callable):
        self.messenger.unsubscribe(callback)

    def get_current_layout(self) -> dict:
        return self.session.get_current_layout().serialize()

    def on_layout_create(self, name: str, callback: Callable[[bool], None]):
        if self.session.check_if_layout_name_is_valid(name):
            layout = Layout(name=name)
            self.session.set_current_layout(layout)
            self.session.save_session()
            callback(True)
        else:
            callback(False)

    def on_layout_select(self, callback: Callable[[None], None]) -> list[tuple[str, str, Callable[[str], None]]]:
        def on_select(content):
            self.session.set_current_layout(self.session.get_layout_by_id(content.id))
            callback(None)
        return [(layout.name, layout.id, on_select) for layout in self.session.get_layouts().values()]

    def on_layout_save(self):
        self.session.save_session()

    def on_layout_cancel(self):
        self.session.discard_session()

    def on_layout_delete(self):
        self.session.remove_layout(self.session.get_current_layout())
        self.session.save_session()

    def get_controllers(self) -> list[dict]:
        return [ctrl.serialize() for ctrl in self.session.get_controllers().values()]

    def on_controller_save(self, controller: dict, callback: Callable[[bool], None]):
        if self.session.check_if_controller_name_is_valid(controller["name"]):
            ctrl = Controller(name=controller["name"], type=controller["type"],
                              custom_name=controller["custom_name"], variable_name=controller["variable_name"],
                              range=controller["range"], position=controller["position"], size=controller["size"])
            self.session.add_controller(ctrl)
            callback(True)
        else:
            callback(False)

    def on_controller_edit_save(self, controller: dict, callback: Callable[[bool], None]):
        ctrl = self.session.get_controller_by_id(controller["id"])
        if self.session.check_if_controller_name_is_valid(controller["name"], [ctrl]):
            ctrl.copy_from_dict(controller)
            callback(True)
        else:
            callback(False)

    def on_controller_move(self, id: str, position: tuple[float, float]):
        ctrl = self.session.get_controller_by_id(id)
        ctrl.position = position

    def on_controller_delete(self, id: str):
        self.session.remove_controller(self.session.get_controller_by_id(id))

    def get_variables(self) -> list[dict]:
        return [var.serialize() for var in self.session.get_variables().values()]

    def on_variable_save(self, variable: dict, callback: Callable[[bool], None]):
        if self.session.check_if_variable_name_is_valid(variable["name"]):
            var = Variable(name=variable["name"], type=variable["type"],
                           direction=variable["direction"], interval=variable["interval"])
            self.session.add_variable(var)
            self.session.save_session()
            callback(True)
        else:
            callback(False)

    def on_variable_edit_save(self, variable: dict, callback: Callable[[bool], None]):
        var = self.session.get_variable_by_id(variable["id"])
        if self.session.check_if_variable_name_is_valid(variable["name"], [var]):
            var.copy_from_dict(variable)
            self.session.save_session()
            callback(True)
        else:
            callback(False)

    def on_variable_delete(self, id: str):
        self.session.remove_variable(self.session.get_variable_by_id(id))
        self.session.save_session()
