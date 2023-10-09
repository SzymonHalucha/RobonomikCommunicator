from __future__ import annotations
import views.base_view as base_view


class BasePresenter:
    def __init__(self, **kwargs):
        self.desktop_view: base_view.BaseView = None
        self.tablet_view: base_view.BaseView = None
        self.mobile_view: base_view.BaseView = None

    def set_desktop_view(self, view: base_view.BaseView) -> base_view.BaseView:
        self.desktop_view = view
        return self.desktop_view

    def set_tablet_view(self, view: base_view.BaseView) -> base_view.BaseView:
        self.tablet_view = view
        return self.tablet_view

    def set_mobile_view(self, view: base_view.BaseView) -> base_view.BaseView:
        self.mobile_view = view
        return self.mobile_view
