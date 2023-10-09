from __future__ import annotations
from kivymd.uix.boxlayout import MDBoxLayout
from views.base_subview import BaseSubview
from views.base_view import BaseView
import views.common.common


class MainMobileView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.open_subview_by_type(ConnectSubview)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.open_subview_by_name(f"{tab_text}Subview")


class ConnectSubview(MDBoxLayout, BaseSubview):
    pass


class Connect2Subview(MDBoxLayout, BaseSubview):
    pass


class SettingsSubview(MDBoxLayout, BaseSubview):
    pass


class Settings2Subview(MDBoxLayout, BaseSubview):
    pass
