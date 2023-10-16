from __future__ import annotations
from kivymd.uix.responsivelayout import MDResponsiveLayout
from kivymd.uix.screen import MDScreen
from views.base_view import BaseView
import views.base_subview as base_subview


class MyRootWidget(MDResponsiveLayout, MDScreen):
    def __init__(self):
        super().__init__()
        self._desktop_views: list[BaseView] = []
        self._tablet_views: list[BaseView] = []
        self._mobile_views: list[BaseView] = []
        self._current_views: list[BaseView] = []
        self._view: BaseView = None
        self._subview: base_subview.BaseSubview = None

    def on_change_screen_type(self, *args):
        first: bool = self._current_views == []
        if args[0] == "desktop":
            self._current_views: list[BaseView] = self._desktop_views
        elif args[0] == "tablet":
            self._current_views: list[BaseView] = self._tablet_views
        elif args[0] == "mobile":
            self._current_views: list[BaseView] = self._mobile_views
        if first:
            self._close_all_views()
            self.open_view_by_index(0)
        else:
            self._subview = self._view.get_current_subview()
            self.open_view_by_name(self._view.name, keep_subview=True)

    def add_desktop_view(self, view: BaseView):
        self._desktop_views.append(view)

    def add_tablet_view(self, view: BaseView):
        self._tablet_views.append(view)

    def add_mobile_view(self, view: BaseView):
        self._mobile_views.append(view)

    def open_view_by_index(self, index: int, **kwargs):
        keep: bool = kwargs.get("keep_subview", False)
        close: bool = kwargs.get("close_subviews", False)
        [self._open_view(view, keep) if i == index else self._close_view(view, close) for i, view in enumerate(self._current_views)]

    def open_view_by_name(self, view_name: str, **kwargs):
        keep: bool = kwargs.get("keep_subview", False)
        close: bool = kwargs.get("close_subviews", False)
        [self._open_view(view, keep) if view.name == view_name else self._close_view(view, close) for view in self._current_views]

    def open_view_by_type(self, view_type: type, **kwargs):
        keep: bool = kwargs.get("keep_subview", False)
        close: bool = kwargs.get("close_subviews", False)
        [self._open_view(view, keep) if isinstance(view, view_type) or issubclass(view_type, type(view))
         else self._close_view(view, close) for view in self._current_views]

    def update_current_view(self):
        [self._open_view(view) for view in self._current_views if view.is_active]

    def _close_all_views(self):
        [self._close_view(view, True) for view in self._desktop_views]
        [self._close_view(view, True) for view in self._tablet_views]
        [self._close_view(view, True) for view in self._mobile_views]

    def _open_view(self, view: BaseView, keep_subview: bool = False):
        if view not in self.children:
            self.add_widget(view)
        view.open(subview_name=self._subview.name if keep_subview else None)
        self._view = view

    def _close_view(self, view: BaseView, close_subviews: bool = False):
        view.close(close_subviews=close_subviews)
        if view in self.children:
            self.remove_widget(view)
