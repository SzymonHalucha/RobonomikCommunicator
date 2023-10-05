from kivy.uix.behaviors import DragBehavior
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.list import IRightBodyTouch, BaseListItem, TwoLineRightIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.card import MDCard
from controller import Controller
from messenger import Messenger
from variable import Variable
from preset import Preset
from layout import Layout
from ui.view import View
from ui.group import Group
import sys


# ==================== Main ==================== #
class TopBar(MDBoxLayout):
    pass


class MyTab(MDFloatLayout, MDTabsBase):
    pass


class MyClosedPortViewGroup(Group):
    def open(self, *args):
        super().open(*args)
        self._app.root.ids.top_bar.right_action_items = []


class MyOpenPortViewGroup(Group):
    def open(self, *args):
        super().open(*args)
        self._app.root.ids.top_bar.right_action_items = [["connection", lambda x: self._app.on_close_port(), "Disconnect"]]


# ==================== Views ==================== #
class BaseView(MDBoxLayout, View):
    pass


class ConnectWindow(BaseView):
    def update(self):
        items = [item for item in self.ids.available_ports_list.children if isinstance(item, MyTwoLineAvatarIconListItem)]
        items_names = [item.text for item in items]
        ports = Messenger.get_available_ports()
        ports_names = [port.device for port in ports]
        for port in ports:
            if port.device not in items_names:
                item = MyTwoLineAvatarIconListItem(text=port.device, secondary_text=port.description)
                self.ids.available_ports_list.add_widget(item)
        for item in items:
            if item.text not in ports_names:
                self.ids.available_ports_list.remove_widget(item)


class SettingsWindow(BaseView):
    def update(self):
        name = self._app.session.get_current_preset().name
        self.ids.preset_name.text = f"Preset: {name}"
        self.ids.default_baudrate.text = f"{self._app.session.default_baudrate}"
        self.ids.show_console_timestamps.ids.checkbox_container.active = self._app.session.show_console_timestamps


class ConsoleWindow(BaseView):
    def open(self, *args):
        super().open(*args)
        self._app.messenger.subscribe(self.update)

    def close(self, *args):
        self._app.messenger.unsubscribe(self.update)
        super().close(*args)

    def update(self, *args):
        history = self._app.messenger.history[-100:]
        show_timestamps = self._app.session.show_console_timestamps
        self.ids.console.text = ""
        for msg in history:
            self.ids.console.text += f"{f'[{msg[0]}] ' if show_timestamps else ''}{'<<< ' if msg[2] else '>>> '}{msg[1]}"
        if self.ids.console_scroll.scroll_y <= 0.01:
            self.ids.console_scroll.scroll_y = 0


class LayoutsWindow(BaseView):
    def update(self):
        self.ids.layout_name.text = f"Layout: {self._app.session.get_current_layout().name}"
        controllers = self._app.session.get_controllers()
        items = [item for item in self.ids.controllers_board.children if isinstance(item, MyBaseControllerCard)]
        items_controllers = [item.controller for item in items]
        for item in items:
            if item.controller not in controllers:
                self.ids.controllers_board.remove_widget(item)
            else:
                item.update_view()
        for controller in controllers:
            if controller not in items_controllers:
                card = getattr(sys.modules[__name__], f"My{controller.type}ControllerCard")
                self.ids.controllers_board.add_widget(card(controller=controller))


class LayoutsEditWindow(BaseView):
    def update(self):
        self.ids.layout_name.text = f"Edit Layout: {self._app.session.get_current_layout().name}"
        controllers = self._app.session.get_controllers()
        items = [item for item in self.ids.controllers_board.children if isinstance(item, MyBaseControllerEditCard)]
        items_controllers = [item.controller for item in items]
        for item in items:
            if item.controller not in controllers:
                self.ids.controllers_board.remove_widget(item)
            else:
                item.update_view()
        for controller in controllers:
            if controller not in items_controllers:
                card = getattr(sys.modules[__name__], f"My{controller.type}ControllerEditCard")
                self.ids.controllers_board.add_widget(card(controller=controller))


class CreateControllerWindow(BaseView):
    pass


class VariablesWindow(BaseView):
    def update(self):
        variables = self._app.session.get_variables()
        items = [item for item in self.ids.variables_list.children if isinstance(item, MyVariableCard)]
        items_variables = [item.variable for item in items]
        for item in items:
            if item.variable not in variables:
                self.ids.variables_list.remove_widget(item)
            else:
                item.update_view()
        for variable in variables:
            if variable not in items_variables:
                item = MyVariableCard(variable=variable)
                self.ids.variables_list.add_widget(item)


class CreateVariableWindow(BaseView):
    pass


# ==================== List ==================== #
class MyListItemWithCheckbox(BaseListItem):
    pass


class MyRightCheckboxContainer(IRightBodyTouch, MDCheckbox):
    pass


class MyTwoLineListItemWithCheckbox(TwoLineRightIconListItem, MyListItemWithCheckbox):
    pass


class MyTwoLineAvatarIconListItem(TwoLineAvatarIconListItem):
    pass


# ==================== Cards ==================== #
class MyVariableCard(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.variable: "Variable" = kwargs["variable"] if "variable" in kwargs else None
        if self.variable is not None:
            self.update_view()

    def update_view(self):
        self.id = self.variable.name
        self.ids.variable_name.text = f"Name: {self.variable.name}"
        self.ids.variable_type.text = f"Type: {self.variable.type}"
        self.ids.variable_direction.text = f"Direction: {self.variable.direction}"
        self.ids.variable_interval.text = f"Refresh: {self.variable.interval}ms"

    def update_reference(self, variable: "Variable"):
        self.variable = variable
        self.update_view()


class MyBaseControllerCard(MDCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.controller: "Controller" = kwargs["controller"] if "controller" in kwargs else None
        Window.bind(size=self.on_window_resize)
        if self.controller is not None:
            self.update_view()

    def update_view(self):
        self.id = self.controller.name
        self.pos = (Window.width * self.controller.position[0], Window.height * self.controller.position[1])
        self.size = dp(self.controller.size[0]), dp(self.controller.size[1])
        self.children[0].ids.controller_name.text = f"{self.controller.name}"
        if "controller_type" in self.children[0].ids:
            self.children[0].ids.controller_type.text = f"{self.controller.type}"
        if "controller_variable" in self.children[0].ids:
            self.children[0].ids.controller_variable.text = f": {self.controller.variable_name}"
        if "controller_custom_name" in self.children[0].ids:
            self.children[0].ids.controller_custom_name.text = f"{self.controller.custom_name}"

    def update_reference(self, controller: "Controller"):
        self.controller = controller
        self.update_view()

    def on_window_resize(self, *args):
        if self.controller is not None:
            self.pos = (args[1][0] * self.controller.position[0], args[1][1] * self.controller.position[1])


class MyTriggerControllerCard(MyBaseControllerCard):
    pass


class MySwitchControllerCard(MyBaseControllerCard):
    pass


class MySliderControllerCard(MyBaseControllerCard):
    pass


class MyInputControllerCard(MyBaseControllerCard):
    pass


class MyBaseControllerEditCard(DragBehavior, MyBaseControllerCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        if self.collide_point(*touch.pos):
            self.controller.position = (self.pos[0] / Window.width, self.pos[1] / Window.height)


class MyTriggerControllerEditCard(MyBaseControllerEditCard):
    pass


class MySwitchControllerEditCard(MyBaseControllerEditCard):
    pass


class MySliderControllerEditCard(MyBaseControllerEditCard):
    pass


class MyInputControllerEditCard(MyBaseControllerEditCard):
    pass


# ==================== Dialogs ==================== #
class MyBaseVariableDialog(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.next_type: "MyBaseVariableDialog" = None
        self.variable: "Variable" = kwargs["variable"] if "variable" in kwargs else None
        if self.variable is not None:
            self.ids.variable_name.text = self.variable.name
            self.ids.variable_type.text = self.variable.type
            self.ids.variable_direction.text = self.variable.direction
            self.ids.variable_interval.text = str(self.variable.interval)

    @property
    def edited_variable(self) -> "Variable":
        return Variable(name=self.ids.variable_name.text,
                        type=self.ids.variable_type.text,
                        direction=self.ids.variable_direction.text,
                        interval=int(self.ids.variable_interval.text if "variable_interval" in self.ids else "0"))

    def on_variable_direction_click(self):
        self.ids.variable_direction.text = "Input" if self.ids.variable_direction.text == "Output" else "Output"

    def on_variable_type_click(self):
        MDApp.get_running_app().on_create_variable(self.next_type())


class MyTriggerVariableDialog(MyBaseVariableDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_type: "MyBaseVariableDialog" = MyIntVariableDialog
        self.ids.variable_type.text = "Trigger"


class MyIntVariableDialog(MyBaseVariableDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_type: "MyBaseVariableDialog" = MyFloatVariableDialog
        self.ids.variable_type.text = "Int"


class MyFloatVariableDialog(MyBaseVariableDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_type: "MyBaseVariableDialog" = MyStringVariableDialog
        self.ids.variable_type.text = "Float"


class MyStringVariableDialog(MyBaseVariableDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_type: "MyBaseVariableDialog" = MyTriggerVariableDialog
        self.ids.variable_type.text = "String"


class MyBaseControllerDialog(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.controller: "Controller" = kwargs["controller"] if "controller" in kwargs else None
        self.next_type: "MyBaseControllerDialog" = MyTriggerControllerDialog
        if self.controller is not None:
            self.ids.controller_name.text = self.controller.name
            self.ids.controller_type.text = self.controller.type
            self.ids.controller_variable.text = self.controller.variable_name
            self.ids.controller_width.text = str(self.controller.size[0])
            self.ids.controller_height.text = str(self.controller.size[1])
            if "controller_custom_name" in self.ids:
                self.ids.controller_custom_name.text = self.controller.custom_name
            if "controller_start_value" in self.ids:
                self.ids.controller_start_value.text = self.controller.start_range
            if "controller_end_value" in self.ids:
                self.ids.controller_end_value.text = self.controller.end_range

    @property
    def edited_controller(self) -> "Controller":
        controller = Controller(name=self.ids.controller_name.text,
                                type=self.ids.controller_type.text,
                                custom_name=self.ids.controller_custom_name.text if "controller_custom_name" in self.ids else "Default",
                                variable_name=self.ids.controller_variable.text,
                                start_value=self.ids.controller_start_value.text if "controller_start_value" in self.ids else "0",
                                end_value=self.ids.controller_end_value.text if "controller_end_value" in self.ids else "0",
                                size=(int(self.ids.controller_width.text), int(self.ids.controller_height.text)),
                                position=(0.5, 0.5))
        return controller

    def on_controller_type_click(self):
        MDApp.get_running_app().on_add_controller(self.next_type())


class MyTriggerControllerDialog(MyBaseControllerDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_type: "MyBaseControllerDialog" = MySwitchControllerDialog
        self.ids.controller_type.text = "Trigger"


class MySwitchControllerDialog(MyBaseControllerDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_type: "MyBaseControllerDialog" = MySliderControllerDialog
        self.ids.controller_type.text = "Switch"


class MySliderControllerDialog(MyBaseControllerDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_type: "MyBaseControllerDialog" = MyInputControllerDialog
        self.ids.controller_type.text = "Slider"


class MyInputControllerDialog(MyBaseControllerDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_type: "MyBaseControllerDialog" = MyTriggerControllerDialog
        self.ids.controller_type.text = "Input"


class MyCreatePresetDialog(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.preset: "Preset" = kwargs["preset"] if "preset" in kwargs else None
        if self.preset is not None:
            self.ids.preset_name.text = self.preset.name

    @property
    def edited_preset(self) -> "Preset":
        return Preset(name=self.ids.preset_name.text)


class MySelectPresetDialog(MDBoxLayout):
    pass


class MyCreateLayoutDialog(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.layout: "Layout" = kwargs["layout"] if "layout" in kwargs else None
        if self.layout is not None:
            self.ids.layout_name.text = self.layout.name

    @property
    def edited_layout(self) -> "Layout":
        return Layout(name=self.ids.layout_name.text)


class MySelectLayoutDialog(MDBoxLayout):
    pass
