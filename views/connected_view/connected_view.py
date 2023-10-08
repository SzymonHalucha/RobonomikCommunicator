from __future__ import annotations
from kivymd.uix.responsivelayout import MDResponsiveLayout
import views.connected_view.desktop.connected_desktop_view as connected_desktop_view
import views.connected_view.mobile.connected_mobile_view as connected_mobile_view
import views.base_view as base_view


class ConnectedView(MDResponsiveLayout, base_view.BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.desktop_view = connected_desktop_view.ConnectedDesktopView()
        self.tablet_view = connected_desktop_view.ConnectedDesktopView()
        self.mobile_view = connected_mobile_view.ConnectedMobileView()
