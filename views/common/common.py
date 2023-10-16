from __future__ import annotations
from kivy.core.window import Window
from kivy.uix.behaviors import DragBehavior
from kivymd.uix.list import BaseListItem, TwoLineRightIconListItem, TwoLineAvatarIconListItem, IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.card import MDCard
import views.base_view as base_view


class MyTab(MDFloatLayout, MDTabsBase):
    pass


class MyListItemWithCheckbox(BaseListItem):
    pass


class MyRightCheckboxContainer(IRightBodyTouch, MDCheckbox):
    pass


class MyTwoLineListItemWithCheckbox(TwoLineRightIconListItem, MyListItemWithCheckbox):
    pass


class MyTwoLineAvatarIconListItem(TwoLineAvatarIconListItem):
    pass


class MyVariableCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__()
        self.view: base_view.BaseView = kwargs.get("view", None)
        self.variable: dict = kwargs.get("variable", None)
        self.update_view(self.variable)

    def update_view(self, variable: dict):
        self.id = self.variable["id"]
        self.ids.variable_name.text = f"Name: {variable['name']}"
        self.ids.variable_type.text = f"Type: {variable['type']}"
        self.ids.variable_direction.text = f"Direction: {variable['direction']}"
        self.ids.variable_interval.text = f"Refresh: {variable['interval']}ms"


class MyBaseControllerCard(MDCard):
    def __init__(self, **kwargs):
        super().__init__()
        self.controller: dict = kwargs.get("controller", None)
        self.update_view(self.controller)
        Window.bind(size=self.on_window_resize)

    def update_view(self, controller: dict):
        self.id = controller["id"]
        self.pos = (Window.width * controller["position"][0], Window.height * controller["position"][1])
        self.size = (controller["size"][0], controller["size"][1])
        if "controller_name" in self.children[0].ids:
            self.children[0].ids.controller_name.text = f"{controller['name']}"
        if "controller_type" in self.children[0].ids:
            self.children[0].ids.controller_type.text = f"{controller['type']}"
        if "controller_variable" in self.children[0].ids:
            self.children[0].ids.controller_variable.text = f": {controller['variable_name']}"
        if "controller_custom_name" in self.children[0].ids:
            self.children[0].ids.controller_custom_name.text = f"{controller['custom_name']}"

    def on_window_resize(self, *args):
        self.pos = (args[1][0] * self.controller["position"][0], args[1][1] * self.controller["position"][1])


class MyButtonControllerCard(MyBaseControllerCard):
    pass


class MySwitchControllerCard(MyBaseControllerCard):
    pass


class MySliderControllerCard(MyBaseControllerCard):
    pass


class MyTextInputControllerCard(MyBaseControllerCard):
    pass


class MyBaseControllerEditCard(DragBehavior, MyBaseControllerCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.view: base_view.BaseView = kwargs.get("view", None)

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        if self.collide_point(*touch.pos):
            self.controller["position"] = (self.pos[0] / Window.width, self.pos[1] / Window.height)
            self.view.on_controller_move(self.controller["id"], self.controller["position"])


class MyButtonControllerEditCard(MyBaseControllerEditCard):
    pass


class MySwitchControllerEditCard(MyBaseControllerEditCard):
    pass


class MySliderControllerEditCard(MyBaseControllerEditCard):
    pass


class MyTextInputControllerEditCard(MyBaseControllerEditCard):
    pass


class MyCreatePresetDialogContent(MDBoxLayout):
    def __init__(self, name: str = "Default"):
        super().__init__()
        self.ids.preset_name.text = name

    @property
    def preset(self) -> str:
        return self.ids.preset_name.text


class MySelectPresetDialogContent(MDBoxLayout):
    pass


class MyCreateLayoutDialogContent(MDBoxLayout):
    def __init__(self, layout_name: str = "Default"):
        super().__init__()
        self.ids.layout_name.text = layout_name

    @property
    def layout(self) -> str:
        return self.ids.layout_name.text


class MySelectLayoutDialogContent(MDBoxLayout):
    pass
