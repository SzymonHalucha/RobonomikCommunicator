from __future__ import annotations
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from views.base_view import BaseView


class MyRootWidget(MDResponsiveLayout, MDScreen):
    def __init__(self, **kwargs):
        super().__init__()
        self.desktop_views: dict[str, BaseView] = {}
        self.tablet_views: dict[str, BaseView] = {}
        self.mobile_views: dict[str, BaseView] = {}

    def on_change_screen_type(self, *args):
        if args[0] == "desktop":
            self.desktop_view.update_current_subview()
        elif args[0] == "tablet":
            self.tablet_view.update_current_subview()
        elif args[0] == "mobile":
            self.mobile_view.update_current_subview()

    def add_desktop_view(self, name: str, view: BaseView):
        self.desktop_views[name] = view
        self.desktop_view = view

    def add_tablet_view(self, name: str, view: BaseView):
        self.tablet_views[name] = view
        self.tablet_view = view

    def add_mobile_view(self, name: str, view: BaseView):
        self.mobile_views[name] = view
        self.mobile_view = view

    def set_view_by_name(self, name: str):
        if name in self.desktop_views:
            self.desktop_view = self.desktop_views[name]
        if name in self.tablet_views:
            self.tablet_view = self.tablet_views[name]
        if name in self.mobile_views:
            self.mobile_view = self.mobile_views[name]
        self.update_screen()
        self.update_current_subview()

    def set_view_by_type(self, view_type: type):
        if view_type.__name__ in self.desktop_views:
            self.desktop_view = self.desktop_views[view_type.__name__]
        if view_type.__name__ in self.tablet_views:
            self.tablet_view = self.tablet_views[view_type.__name__]
        if view_type.__name__ in self.mobile_views:
            self.mobile_view = self.mobile_views[view_type.__name__]
        self.update_screen()
        self.update_current_subview()

    def update_current_subview(self):
        if self._current_device_type == "desktop":
            self.desktop_view.update_current_subview()
        elif self._current_device_type == "tablet":
            self.tablet_view.update_current_subview()
        elif self._current_device_type == "mobile":
            self.mobile_view.update_current_subview()

    def get_current_view(self) -> BaseView:
        return self.desktop_view \
            if self._current_device_type == "desktop" \
            else self.tablet_view \
            if self._current_device_type == "tablet" \
            else self.mobile_view

    def get_view_by_name(self, name: str) -> BaseView:
        return self.desktop_views[name] \
            if self._current_device_type == "desktop" \
            else self.tablet_views[name] \
            if self._current_device_type == "tablet" \
            else self.mobile_views[name]

    def update_screen(self):
        self.clear_widgets()
        if self.mobile_view and self.tablet_view and self.desktop_view:
            if self.real_device_type == "mobile":
                self.add_widget(self.mobile_view)
            elif self.real_device_type == "tablet":
                self.add_widget(self.tablet_view)
            elif self.real_device_type == "desktop":
                self.add_widget(self.desktop_view)
