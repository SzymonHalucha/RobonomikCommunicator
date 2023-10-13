from __future__ import annotations
from ast import arg
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivymd.uix.list import OneLineAvatarListItem, BaseListItem
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from typing import Callable


class Dialoger:
    def __init__(self):
        self._confirm_dialog: MDDialog
        self._delete_dialog: MDDialog
        self._list_dialog: MDDialog
        self.initialize_dialogs()

    def show_name_error(self, id: str, item_name: str):
        self._confirm_dialog.content_cls.ids[id].helper_text = f"{item_name} name already exists or is invalid"
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

    def close_dialogs(self, *args):
        if len(args) <= 0 or self._confirm_dialog is not args[0]:
            self._confirm_dialog.dismiss()
        if len(args) <= 0 or self._delete_dialog is not args[0]:
            self._delete_dialog.dismiss()
        if len(args) <= 0 or self._list_dialog is not args[0]:
            self._list_dialog.dismiss()

    def open_confirm_dialog(self, title: str, content: MDBoxLayout, on_confirm: Callable[[Widget], None], **kwargs):
        def on_cancel():
            kwargs["on_cancel"](self._confirm_dialog.content_cls) if "on_cancel" in kwargs else self.close_dialogs()

        self.close_dialogs(self._confirm_dialog)
        self._confirm_dialog.title = title
        self._confirm_dialog.ids.spacer_top_box.remove_widget(self._confirm_dialog.content_cls)
        self._confirm_dialog.content_cls = content
        self._confirm_dialog.ids.spacer_top_box.add_widget(self._confirm_dialog.content_cls)
        self._confirm_dialog.buttons[0].on_release = lambda *x: on_cancel()
        self._confirm_dialog.buttons[1].on_release = lambda *x: on_confirm(self._confirm_dialog.content_cls)
        Clock.schedule_once(self._confirm_dialog.update_height)
        Clock.schedule_once(self._confirm_dialog.update_width)
        self._confirm_dialog.open()

    def open_delete_dialog(self, title: str, text: str, on_delete: Callable[[None], None], **kwargs):
        def on_cancel():
            kwargs["on_cancel"](self._delete_dialog.content_cls) if "on_cancel" in kwargs else self.close_dialogs()

        self.close_dialogs(self._delete_dialog)
        self._delete_dialog.title = title
        self._delete_dialog.text = text
        self._delete_dialog.buttons[0].on_release = lambda *x: on_cancel()
        self._delete_dialog.buttons[1].on_release = lambda *x: on_delete(None)
        Clock.schedule_once(self._delete_dialog.update_width)
        self._delete_dialog.open()

    def open_list_dialog(self, title: str, items: list[tuple[str, Callable[[str], None]]]):
        def on_select(item_name: str, func: Callable[[str], None]):
            func(item_name)
            self.close_dialogs()

        self.close_dialogs(self._list_dialog)
        self._list_dialog.title = title
        self._list_dialog.ids.box_items.clear_widgets()
        self._list_dialog.items = (OneLineAvatarListItem(text=item[0], divider=None, on_release=lambda x: on_select(x.text, item[1])) for item in items)
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
