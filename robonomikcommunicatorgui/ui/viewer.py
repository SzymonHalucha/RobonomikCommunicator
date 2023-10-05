from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from messenger import Messenger
from session import Session
from saver import Saver
from ui.group import Group
import logger


@logger.trace_class
class Viewer:
    def __init__(self):
        self._saver: "Saver" = None
        self._messenger: "Messenger" = None
        self._session: "Session" = None
        self._root: "MDBoxLayout" = None
        self._groups: list[Group] = []
        self._current_group: "Group" = None

    def get_references(self):
        app = MDApp.get_running_app()
        self._saver: "Saver" = app.saver
        self._messenger: "Messenger" = app.messenger
        self._session: "Session" = app.session
        self._root: "MDBoxLayout" = app.root

    def open_view_by_type(self, view_type: "type"):
        self._current_group.open_view_by_type(view_type)

    def update_current_view(self):
        self._current_group.update_opened_views()

    def register_group(self, group: "Group"):
        if group not in self._groups:
            self._groups.append(group)

    def unregister_group(self, group: "Group"):
        if group in self._groups:
            self._groups.remove(group)
        if self._current_group == group:
            self._current_group = None

    def open_group_by_type(self, group_type: "type"):
        [self._set_current_group(group) if isinstance(group, group_type) else group.close() for group in self._groups]

    def _set_current_group(self, group: "Group"):
        self._current_group = group
        group.open()
