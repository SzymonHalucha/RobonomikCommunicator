from __future__ import annotations
from typing import Callable
from presenters.base_presenter import BasePresenter
from models.messenger import Messenger
from models.session import Session


class ConnectedPresenter(BasePresenter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messenger: Messenger = kwargs.get("messenger", None)
        self.session: Session = kwargs.get("session", None)

    def on_message_send(self, text: str, callback: Callable[[tuple[list[tuple[str, str, bool]], bool]], None] = None):
        if text == "":
            return
        self.messenger.send(text)
        if callback is not None:
            callback(self.messenger.history[-150:], self.session.show_console_timestamps)

    def get_messages_history(self) -> tuple[list[tuple[str, str, bool]], bool]:
        return (self.messenger.history[-150:], self.session.show_console_timestamps)

    def listen_for_messages_from_serial(self, callback: Callable):
        if callback is not None:
            self.messenger.subscribe(callback)

    def stop_listen_for_messages_from_serial(self, callback: Callable):
        if callback is not None:
            self.messenger.unsubscribe(callback)

    def get_variables(self) -> list[tuple[str, str, str, int]]:
        return [(var.name, var.type, var.direction, var.interval) for var in self.session.get_variables()]
