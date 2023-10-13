from __future__ import annotations
from typing import Callable
from presenters.base_presenter import BasePresenter
from models.variable import Variable
from models.layout import Layout
from models.messenger import Messenger
from models.session import Session


class ConnectedPresenter(BasePresenter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messenger: Messenger = kwargs.get("messenger", None)
        self.session: Session = kwargs.get("session", None)

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

    def get_current_layout(self) -> tuple[str, list[dict]]:
        ctrls = [ctrl.serialize() for ctrl in self.session.get_controllers()]
        return (self.session.get_current_layout().name, ctrls)

    def on_layout_create(self, layout_name: str, callback: Callable[[bool], None]):
        layout = Layout(name=layout_name)
        if self.session.check_if_layout_is_valid(layout):
            self.session.set_current_layout(layout)
            self.session.save_session()
            callback(True)
        else:
            callback(False)

    def on_layout_select(self, callback: Callable[[None], None]) -> list[tuple[str, Callable[[str], None]]]:
        def on_select(name: str):
            self.session.set_current_layout(self.session.get_layout_by_name(name))
            callback(None)
        return [(layout.name, on_select) for layout in self.session.get_layouts()]

    def on_layout_delete(self, callback: Callable[[None], None]):
        self.session.remove_layout(self.session.get_current_layout())
        self.session.save_session()
        callback(None)

    def get_variables(self) -> list[dict]:
        return [var.serialize() for var in self.session.get_variables()]

    def on_variable_save(self, variable: tuple[str, str, str, int], callback: Callable[[bool], None]):
        var = Variable(name=variable[0], type=variable[1], direction=variable[2], interval=variable[3])
        if self.session.check_if_variable_is_valid(var):
            self.session.add_variable(var)
            self.session.save_session()
            callback(True)
        else:
            callback(False)

    def on_variable_edit_save(self, old: tuple[str, str, str, int], new: tuple[str, str, str, int], callback: Callable[[bool], None]):
        old_var = self.session.get_variable_by_name(old[0])
        new_var = Variable(name=new[0], type=new[1], direction=new[2], interval=new[3])
        if self.session.check_if_variable_is_valid(new_var, [old_var]):
            self.session.replace_variable(old_var, new_var)
            self.session.save_session()
            callback(True)
        else:
            callback(False)

    def on_variable_delete(self, variable_name: str, callback: Callable[[None], None]):
        self.session.remove_variable(self.session.get_variable_by_name(variable_name))
        self.session.save_session()
        callback(None)
