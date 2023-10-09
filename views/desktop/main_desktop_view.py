from __future__ import annotations
from kivymd.uix.boxlayout import MDBoxLayout
from views.base_subview import BaseSubview
from views.base_view import BaseView
import views.common.common


class MainDesktopView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.open_subview_by_type(ConnectDesktopSubview)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.open_subview_by_name(f"{tab_text}DesktopSubview")


class ConnectDesktopSubview(MDBoxLayout, BaseSubview):
    pass


class Connect2DesktopSubview(MDBoxLayout, BaseSubview):
    pass


class SettingsDesktopSubview(MDBoxLayout, BaseSubview):
    pass


class Settings2DesktopSubview(MDBoxLayout, BaseSubview):
    pass
