from kivymd.uix.responsivelayout import MDResponsiveLayout
from View.base_screen import BaseScreenView
from View.MainScreen.components import (
    DesktopScreenView,
    MobileScreenView
)


class MainScreenView(BaseScreenView, MDResponsiveLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.desktop_view = DesktopScreenView()
        self.mobile_view = MobileScreenView()
