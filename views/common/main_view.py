from __future__ import annotations
from views.base_view import BaseView
from views.base_subview import BaseSubview
import presenters.main_presenter as main_presenter
import views.common.connected_view as connected_view
import views.common.common as common


class MainView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: main_presenter.MainPresenter = kwargs.get("presenter", None)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.open_subview_by_name(f"{tab_text}Subview")

    def on_ports_list_refresh(self):
        def on_refresh(*args):
            subview = self.get_current_subview()
            if subview is not None:
                subview.update_ports(*args)
        self.presenter.on_ports_list_refresh(on_refresh)

    def on_port_select(self, port: str):
        self.presenter.on_port_select(port)
        self._root.open_view_by_type(connected_view.ConnectedView)

    def on_preset_create(self):
        def on_create(content):
            self.presenter.on_preset_create(content.preset, lambda success: self._dialoger.close_dialogs() if success
                                            else self._dialoger.show_name_error("preset_name", "Preset"))
            self.update_current_subview()
        self._dialoger.open_confirm_dialog("Create Preset", common.MyCreatePresetDialogContent(), on_create)

    def on_preset_delete(self):
        def on_delete(*args):
            self._dialoger.close_dialogs()
            self.presenter.on_preset_delete()
            self.update_current_subview()
        self._dialoger.open_delete_dialog("Delete Preset", "Are you sure you want to delete this preset?", on_delete)

    def on_preset_select(self):
        self._dialoger.open_list_dialog("Select Preset", self.presenter.on_preset_select(self.update_current_subview))

    def on_settings_changed(self, key: str, value):
        self.presenter.on_settings_changed(key, value)


class ConnectSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: main_presenter.MainPresenter = self.presenter

    def update(self):
        self.update_ports(self.presenter.on_ports_list_refresh(lambda *x: None))

    def update_ports(self, ports: list[tuple[str, str]]):
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


class SettingsSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: main_presenter.MainPresenter = self.presenter

    def update(self):
        self.update_settings(self.presenter.get_dict_of_settings())

    def update_settings(self, settings: dict):
        self.ids.preset_name.text = f"Preset: {settings['preset_name']}"
        self.ids.default_baudrate.text = f"{settings['default_baudrate']}"
        checkbox = self.ids.show_console_timestamps.ids.checkbox_container
        checkbox.active = settings["show_console_timestamps"]
        checkbox.on_release = lambda: self.view.on_settings_changed("show_console_timestamps", checkbox.active)
