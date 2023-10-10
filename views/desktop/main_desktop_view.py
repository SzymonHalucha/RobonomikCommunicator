from __future__ import annotations
from kivymd.uix.boxlayout import MDBoxLayout
from views.base_subview import BaseSubview
from views.base_view import BaseView
import presenters.main_presenter as main_presenter
import views.common.common as common


class ConnectDesktopSubview(MDBoxLayout, BaseSubview):
    def update(self, **kwargs):
        if "ports" in kwargs:
            self.update_ports(kwargs["ports"])

    def update_ports(self, ports: list[str, str]):
        items = [item for item in self.ids.ports_list.children if isinstance(item, common.MyTwoLineAvatarIconListItem)]
        items_names = [item.text for item in items]
        ports_names = [port[0] for port in ports]
        for name, desc in ports:
            if name not in items_names:
                item = common.MyTwoLineAvatarIconListItem(text=name, secondary_text=desc, on_release=lambda x: self.view.on_port_select(x.text))
                self.ids.ports_list.add_widget(item)
        for item in items:
            if item.text not in ports_names:
                self.ids.ports_list.remove_widget(item)


class SettingsDesktopSubview(MDBoxLayout, BaseSubview):
    def update(self, **kwargs):
        if "settings" in kwargs:
            self.update_settings(kwargs["settings"])

    def update_settings(self, settings: dict):
        self.ids.preset_name.text = f"Preset: {settings['preset_name']}"
        self.ids.default_baudrate.text = f"{settings['default_baudrate']}"
        checkbox = self.ids.show_console_timestamps.ids.checkbox_container
        checkbox.active = settings["show_console_timestamps"]
        checkbox.on_release = lambda: self.view.on_settings_update("show_console_timestamps", checkbox.active)


class MainDesktopView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._presenter: main_presenter.MainPresenter = kwargs.get("presenter", None)
        self.open_subview_by_type(ConnectDesktopSubview)

    def update_current_subview(self, **kwargs):
        [subview.update(ports=self._presenter.on_ports_list_refresh())
         if isinstance(subview, ConnectDesktopSubview)
         else subview.update(settings=self._presenter.get_dict_of_settings())
         if isinstance(subview, SettingsDesktopSubview)
         else subview.update(**kwargs)
         for subview in self._subviews
         if subview.is_active]

    def on_settings_update(self, *args):
        self._presenter.on_settings_update(*args)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.open_subview_by_name(f"{tab_text}DesktopSubview")

    def on_ports_list_refresh(self):
        self._presenter.on_ports_list_refresh(self.get_current_subview().update_ports)

    def on_port_select(self, port: str):
        self._presenter.on_port_select(port, lambda: self.open_view_by_name("Connected"))

    def on_preset_create(self):
        def on_confirm(content: MyCreatePresetDialogContent):
            self._presenter.on_preset_create(content.edited, lambda success: self._dialoger.close_dialogs() if success
                                             else self._dialoger.show_text_field_error("preset_name", "Preset name is not valid"))
            self.update_current_subview()
        self._dialoger.open_confirm_dialog("Create Preset", MyCreatePresetDialogContent(), on_confirm)

    def on_preset_select(self):
        self._dialoger.open_list_dialog("Select Preset", self._presenter.on_preset_select(self.update_current_subview))

    def on_preset_delete(self):
        def on_delete():
            self._presenter.on_preset_delete(self._dialoger.close_dialogs())
            self.update_current_subview()
        self._dialoger.open_delete_dialog("Delete Preset", "Are you sure you want to delete this preset?", on_delete)


class MyCreatePresetDialogContent(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.name: str = kwargs.get("name", "Default")
        self.ids.preset_name.text = self.name

    @property
    def edited(self) -> str:
        return self.ids.preset_name.text


class MySelectPresetDialogContent(MDBoxLayout):
    pass
