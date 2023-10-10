from __future__ import annotations
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from views.base_view import BaseView


class MyRootWidget(MDResponsiveLayout, MDScreen):
    def __init__(self):
        super().__init__()
        self._desktop_views: list[BaseView] = []
        self._tablet_views: list[BaseView] = []
        self._mobile_views: list[BaseView] = []
        self._current_views: list[BaseView] = []
        self._view_name: str = ""

    def on_change_screen_type(self, *args):
        first: bool = (len(self._current_views) == 0)
        if args[0] == "desktop":
            self._current_views = self._desktop_views
        elif args[0] == "tablet":
            self._current_views = self._tablet_views
        elif args[0] == "mobile":
            self._current_views = self._mobile_views
        self.open_view_by_index(0) if first else self.update_current_view()

    def add_desktop_view(self, view: BaseView):
        self._desktop_views.append(view)

    def add_tablet_view(self, view: BaseView):
        self._tablet_views.append(view)

    def add_mobile_view(self, view: BaseView):
        self._mobile_views.append(view)

    def open_view_by_index(self, index: int):
        [self._open_view(view) if i == index else self._close_view(view) for i, view in enumerate(self._current_views)]

    def open_view_by_name(self, name: str):
        [self._open_view(view) if view.name == name else self._close_view(view) for view in self._current_views]

    def open_view_by_type(self, view_type: type):
        [self._open_view(view) if isinstance(view, view_type) else self._close_view(view) for view in self._current_views]

    def update_current_view(self):
        [self._open_view(view) for view in self._current_views if view.is_active]
        self.open_view_by_name(self._view_name)

    def get_current_view(self) -> BaseView | None:
        return next(iter(view for view in self._current_views if view.is_active), None)

    def _open_view(self, view: BaseView):
        if view not in self.children:
            self.add_widget(view)
        self._view_name = view.name
        view.open()

    def _close_view(self, view: BaseView):
        view.close()
        if view in self.children:
            self.remove_widget(view)
