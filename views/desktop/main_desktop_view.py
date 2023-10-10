from __future__ import annotations
from kivymd.uix.boxlayout import MDBoxLayout
from views.base_subview import BaseSubview
from views.base_view import BaseView
import views.common.common


class ConnectDesktopSubview(MDBoxLayout, BaseSubview):
    pass


class SettingsDesktopSubview(MDBoxLayout, BaseSubview):
    pass


class MainDesktopView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.open_subview_by_type(ConnectDesktopSubview)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.open_subview_by_name(f"{tab_text}DesktopSubview")

    def on_ports_list_refresh(self):
        print("on_ports_list_refresh")

    def on_port_select(self):
        print("on_port_select")

    def on_preset_create(self):
        print("on_preset_create")

    def on_preset_select(self):
        print("on_preset_select")

    def on_preset_delete(self):
        print("on_preset_delete")
