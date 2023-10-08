from __future__ import annotations
from kivymd.uix.responsivelayout import MDResponsiveLayout
import views.main_view.desktop.main_desktop_view as main_desktop_view
import views.main_view.mobile.main_mobile_view as main_mobile_view
import views.common.common as common
import views.base_view as base_view


class MainView(MDResponsiveLayout, base_view.BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.desktop_view = main_desktop_view.MainDesktopView()
        self.tablet_view = main_desktop_view.MainDesktopView()
        self.mobile_view = main_mobile_view.MainMobileView()

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        print("on_tab_switch", instance_tabs, instance_tab, instance_tab_label, tab_text)
