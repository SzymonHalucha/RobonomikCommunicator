from kivymd.uix.responsivelayout import MDResponsiveLayout
from View import BaseView
from View.MainView.platforms import (
    DesktopView,
    MobileView
)


class MainView(BaseView, MDResponsiveLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.desktop_view = DesktopView()
        self.tablet_view = DesktopView()
        self.mobile_view = MobileView()
