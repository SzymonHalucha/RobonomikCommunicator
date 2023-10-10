from __future__ import annotations
from views.base_view import BaseView
from views.base_subview import BaseSubview


class MainView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("MainView: init")

    def on_release(self):
        self.open_subview_by_type(SettingsSubview)

    def on_release1(self):
        self.open_subview_by_type(ConnectSubview)


class MainDesktopView(MainView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("MainView: Desktop")


class MainMobileView(MainView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("MainView: Mobile")


class ConnectSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("ConnectSubview: init")

    def update(self, **kwargs):
        print("ConnectSubview: update")


class ConnectDesktopSubview(ConnectSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("ConnectSubview: Desktop")


class ConnectMobileSubview(ConnectSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("ConnectSubview: Mobile")


class SettingsSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("SettingsSubview: init")

    def update(self, **kwargs):
        print("SettingsSubview: update")


class SettingsDesktopSubview(SettingsSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("SettingsSubview: Desktop")


class SettingsMobileSubview(SettingsSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("SettingsSubview: Mobile")
