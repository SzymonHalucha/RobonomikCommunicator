from kivymd.uix.list import OneLineAvatarListItem, BaseListItem
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.clock import Clock
from controller import Controller
from variable import Variable
from session import Session
from typing import Callable
from ui.viewer import Viewer
import ui.styles as styles
import logger


@logger.trace_class
class Dialoger:
    def __init__(self):
        self._session: Session = None
        self._viewer: "Viewer" = None
        self._confirm_dialog: "MDDialog" = None
        self._delete_dialog: "MDDialog" = None
        self._list_dialog: "MDDialog" = None
        self._show_input_error: "bool" = False

    def get_references(self):
        app = MDApp.get_running_app()
        self._session: "Session" = app.session
        self._viewer: "Viewer" = app.viewer
        self.initialize_dialogs()

    def show_create_preset_dialog(self, callback: "Callable" = None):
        self.open_confirm_dialog("Create Preset", styles.MyCreatePresetDialog(), on_confirm=callback)

    def show_select_preset_dialog(self, callback: "Callable" = None):
        self.open_list_dialog("Select Preset", ((preset.name, callback) for preset in self._session.get_presets()))

    def show_delete_preset_dialog(self, callback: "Callable" = None):
        self.open_delete_dialog("Delete Preset", "Are you sure you want to delete this preset?", on_delete=callback)

    def show_create_variable_dialog(self, content: "styles.MyBaseVariableDialog" = None, callback: "Callable" = None):
        self.open_confirm_dialog("Create Variable", styles.MyTriggerVariableDialog() if content is None else content, on_confirm=callback)

    def show_edit_variable_dialog(self, variable: "Variable", callback: "Callable" = None):
        self.open_confirm_dialog("Edit Variable", styles.MyBaseVariableDialog(variable=variable), on_confirm=callback)

    def show_delete_variable_dialog(self, callback: "Callable" = None):
        self.open_delete_dialog("Delete Variable", "Are you sure you want to delete this variable?", on_delete=callback)

    def show_create_layout_dialog(self, callback: "Callable" = None):
        self.open_confirm_dialog("Create Layout", styles.MyCreateLayoutDialog(), on_confirm=callback)

    def show_select_layout_dialog(self, callback: "Callable" = None):
        self.open_list_dialog("Select Layout", ((layout.name, callback) for layout in self._session.get_layouts()))

    def show_delete_layout_dialog(self, callback: "Callable" = None):
        self.open_delete_dialog("Delete Layout", "Are you sure you want to delete this layout?", on_delete=callback)

    # def show_edit_controller_dialog(self, controller: "Controller", callback: "Callable" = None):
    #     self.open_confirm_dialog("Edit Controller", styles.MyBaseControllerDialog(controller=controller), on_confirm=callback)

    def show_delete_controller_dialog(self, callback: "Callable" = None):
        self.open_delete_dialog("Delete Controller", "Are you sure you want to delete this controller?", on_delete=callback)

    def show_text_field_error(self, id: "str", error: "str"):
        self._confirm_dialog.content_cls.ids[id].helper_text = f"{error}"
        self._confirm_dialog.content_cls.ids[id].error = True
        self._show_input_error = True

    def initialize_dialogs(self):
        self._confirm_dialog = MDDialog(title="Confirm", type="custom", content_cls=MDBoxLayout(), auto_dismiss=False, buttons=[
            MDFlatButton(text="CANCEL", on_release=lambda x: self.close_dialogs()),
            MDRaisedButton(text="CONFIRM")])
        self._delete_dialog = MDDialog(title="Delete", text="Description", type="simple", auto_dismiss=False, buttons=[
            MDFlatButton(text="CANCEL", on_release=lambda x: self.close_dialogs()),
            MDRaisedButton(text="DELETE")])
        self._list_dialog = MDDialog(title="Select", type="simple")

    def close_dialogs(self, ignore_dialog: "MDDialog" = None):
        if self._confirm_dialog is not ignore_dialog:
            self._confirm_dialog.dismiss()
        if self._delete_dialog is not ignore_dialog:
            self._delete_dialog.dismiss()
        if self._list_dialog is not ignore_dialog:
            self._list_dialog.dismiss()

    def open_confirm_dialog(self, title: "str", content: "MDBoxLayout", **kwargs):
        def cancel_callback():
            kwargs["on_cancel"](self._confirm_dialog.content_cls) if "on_cancel" in kwargs else self.close_dialogs()

        def confirm_callback():
            kwargs["on_confirm"](self._confirm_dialog.content_cls) if "on_confirm" in kwargs else self.close_dialogs()
            if self._show_input_error:
                self._show_input_error = False
            else:
                self.close_dialogs()
        self.close_dialogs(self._confirm_dialog)
        self._confirm_dialog.title = title
        self._confirm_dialog.ids.spacer_top_box.remove_widget(self._confirm_dialog.content_cls)
        self._confirm_dialog.content_cls = content
        self._confirm_dialog.ids.spacer_top_box.add_widget(self._confirm_dialog.content_cls)
        self._confirm_dialog.buttons[0].on_release = lambda *x: cancel_callback()
        self._confirm_dialog.buttons[1].on_release = lambda *x: confirm_callback()
        Clock.schedule_once(self._confirm_dialog.update_height)
        Clock.schedule_once(self._confirm_dialog.update_width)
        self._confirm_dialog.open()

    def open_delete_dialog(self, title: "str", text: "str", **kwargs):
        def cancel_callback():
            kwargs["on_cancel"](self._delete_dialog.content_cls) if "on_cancel" in kwargs else self.close_dialogs()

        def delete_callback():
            kwargs["on_delete"](self._delete_dialog.content_cls) if "on_delete" in kwargs else self.close_dialogs()
            if not self._show_input_error:
                self.close_dialogs()
                self._show_input_error = False
        self.close_dialogs(self._delete_dialog)
        self._delete_dialog.title = title
        self._delete_dialog.text = text
        self._delete_dialog.buttons[0].on_release = lambda *x: cancel_callback()
        self._delete_dialog.buttons[1].on_release = lambda *x: delete_callback()
        Clock.schedule_once(self._delete_dialog.update_width)
        self._delete_dialog.open()

    def open_list_dialog(self, title: "str", items: "list[(str, Callable)]"):
        def callback(item_name: "str", func: "Callable"):
            func(item_name)
            self.close_dialogs()
        self.close_dialogs(self._list_dialog)
        self._list_dialog.title = title
        self._list_dialog.ids.box_items.clear_widgets()
        self._list_dialog.items = (OneLineAvatarListItem(text=item[0], divider=None, on_release=lambda x: callback(x.text, item[1])) for item in items)
        self._list_dialog.height = 0
        for item in self._list_dialog.items:
            if isinstance(item, BaseListItem):
                self._list_dialog.height += item.height
                self._list_dialog.edit_padding_for_item(item)
                self._list_dialog.ids.box_items.add_widget(item)
        if self._list_dialog.ids.scroll.height > Window.height * 0.75:
            self._list_dialog.ids.scroll.height = self._list_dialog.get_normal_height()
        else:
            self._list_dialog.ids.scroll.height = self._list_dialog.height
        Clock.schedule_once(self._list_dialog.update_width)
        self._list_dialog.open()
