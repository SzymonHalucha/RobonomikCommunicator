from __future__ import annotations
from kivymd.uix.responsivelayout import MDResponsiveLayout
import View.MainView.platforms.DesktopView.desktop_view as desktop_view
import View.MainView.platforms.MobileView.mobile_view as mobile_view
import View.base_view as base_view


class MainView(base_view.BaseView, MDResponsiveLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.desktop_view = desktop_view.DesktopView()
        self.tablet_view = desktop_view.DesktopView()
        self.mobile_view = mobile_view.MobileView()