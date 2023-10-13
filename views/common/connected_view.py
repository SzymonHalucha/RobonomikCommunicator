from __future__ import annotations
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.behaviors import DragBehavior
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import BaseButton
from kivymd.uix.card import MDCard
from views.base_view import BaseView
from views.base_subview import BaseSubview
import views.common.common as common
import presenters.connected_presenter as connected_presenter
import sys


class ConnectedView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = kwargs.get("presenter", None)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.open_subview_by_name(f"{tab_text}Subview")

    def on_message_send(self, instance: MDTextField):
        def on_send(*args):
            instance.text = ""
            subview = self.get_current_subview()
            if subview is not None:
                subview.update_console(args)
        self.presenter.on_message_send(instance.text, on_send)

    def on_layout_create(self):
        def on_create(content):
            self.presenter.on_layout_create(content.edited, lambda success: self._dialoger.close_dialogs() if success else
                                            self._dialoger.show_name_error("layout_name", "Layout"))
            self.update_current_subview()
        self._dialoger.open_confirm_dialog("Create Layout", MyCreateLayoutDialogContent(), on_create)

    def on_layout_edit(self):
        self.open_subview_by_type(LayoutsEditSubview)

    def on_layout_cancel(self):
        self.open_subview_by_type(LayoutsSubview)

    def on_layout_select(self):
        self._dialoger.open_list_dialog("Select Layout", self.presenter.on_layout_select(self.update_current_subview))

    def on_layout_delete(self):
        def on_delete(*args):
            self.presenter.on_layout_delete(self._dialoger.close_dialogs)
            self.update_current_subview()
        self._dialoger.open_delete_dialog("Delete Layout", "Are you sure you want to delete this layout?", on_delete)

    def on_controller_add(self):
        self.open_subview_by_type(ControllerCreateSubview)

    def on_controller_cancel(self):
        self.open_subview_by_type(LayoutsEditSubview)

    def on_variable_add(self):
        self.open_subview_by_type(VariableCreateSubview)

    # TODO: Change to dropdown menu
    def on_variable_type_click(self, instance: BaseButton):
        if instance.text == "Int":
            instance.text = "Float"
        elif instance.text == "Float":
            instance.text = "String"
        else:
            instance.text = "Int"

    # TODO: Change to dropdown menu
    def on_variable_direction_click(self, instance: BaseButton):
        if instance.text == "Input":
            instance.text = "Output"
        else:
            instance.text = "Input"

    def on_variable_edit(self, instance: MyVariableCard):
        self.open_subview_by_type(VariableCreateSubview)
        subview = self.get_current_subview()
        if subview is not None:
            subview.set_values(instance.variable)

    def on_variable_delete(self, instance: MyVariableCard):
        def on_delete(*args):
            self.presenter.on_variable_delete(instance.variable[0], self._dialoger.close_dialogs)
            self.update_current_subview()
        self._dialoger.open_delete_dialog("Delete Variable", "Are you sure you want to delete this variable?", on_delete)

    def on_variable_edit_save(self, instance: VariableCreateSubview):
        self.presenter.on_variable_edit_save(instance.variable, instance.edited, lambda success: self.open_subview_by_type(VariablesSubview)
                                             if success else instance.show_error())

    def on_variable_save(self, instance: VariableCreateSubview):
        self.presenter.on_variable_save(instance.edited, lambda success: self.open_subview_by_type(VariablesSubview)
                                        if success else instance.show_error())

    def on_variable_cancel(self):
        self.open_subview_by_type(VariablesSubview)


class ConsoleSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = self.presenter

    def open(self):
        super().open()
        self.presenter.listen_for_messages_from_serial(self.update)

    def close(self):
        self.presenter.stop_listen_for_messages_from_serial(self.update)
        super().close()

    def update(self, *args):
        self.update_console(self.presenter.get_messages_history())

    def update_console(self, history: tuple[list[tuple[str, str, bool]], bool]):
        self.ids.console.text = ""
        for msg in history[0]:
            self.ids.console.text += f"{f'[{msg[0]}] ' if history[1] else ''}{'<<< ' if msg[2] else '>>> '}{msg[1]}"
        if self.ids.console_scroll.scroll_y <= 0.01:
            self.ids.console_scroll.scroll_y = 0


class LayoutsSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = self.presenter

    def update(self):
        layout = self.presenter.get_current_layout()
        self.update_layout_board(layout[0], layout[1])

    def update_layout_board(self, layout_name: str, controllers: list[dict]):
        self.ids.layout_name.text = f"Layout: {layout_name}"
        self.ids.controllers_board.clear_widgets()
        for controller in controllers:
            class_name = f"My{controller[1].replace(' ', '')}ControllerCard"
            self.ids.controllers_board.add_widget(getattr(sys.modules[__name__], class_name(controller=controller)))


class LayoutsEditSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = self.presenter

    def update(self):
        layout = self.presenter.get_current_layout()
        self.update_layout_board(layout[0], layout[1])

    def update_layout_board(self, layout_name: str, controllers: list[dict]):
        self.ids.layout_name.text = f"Edit Layout: {layout_name}"
        self.ids.controllers_board.clear_widgets()
        for controller in controllers:
            class_name = f"My{controller[1].replace(' ', '')}ControllerEditCard"
            self.ids.controllers_board.add_widget(getattr(sys.modules[__name__], class_name(controller=controller)))


class ControllerCreateSubview(BaseSubview):
    def update(self):
        pass


class VariablesSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = self.presenter

    def update(self):
        self.update_variables_list(self.presenter.get_variables())

    def update_variables_list(self, variables: list[dict]):
        self.ids.variables_list.clear_widgets()
        [self.ids.variables_list.add_widget(MyVariableCard(self.view, var)) for var in variables]


class VariableCreateSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = self.presenter

    def open(self):
        super().open()
        self.ids.variable_name.error = False
        self.ids.variable_name.helper_text = ""
        self.ids.variable_save.on_release = lambda *x: self.view.on_variable_save(self)

    def update(self):
        pass

    def show_error(self):
        self.ids.variable_name.helper_text = "Variable name already exists or is invalid"
        self.ids.variable_name.error = True

    def set_values(self, values: dict):
        self.variable: dict = values
        self.ids.variable_save.on_release = lambda *x: self.view.on_variable_edit_save(self)
        self.ids.variable_name.text = values["name"]
        self.ids.variable_type.text = values["type"]
        self.ids.variable_direction.text = values["direction"]
        self.ids.variable_interval.text = str(values["interval"])

    @property
    def edited(self) -> dict:
        return {"name": self.ids.variable_name.text, "type": self.ids.variable_type.text,
                "direction": self.ids.variable_direction.text, "interval": int(self.ids.variable_interval.text)}


class MyVariableCard(MDCard):
    def __init__(self, view: BaseView, variable: dict):
        super().__init__()
        self.view: BaseView = view
        self.variable: dict = variable
        self.update_view(variable)

    def update_view(self, variable: dict):
        self.id = self.variable["name"]
        self.ids.variable_name.text = f"Name: {variable['name']}"
        self.ids.variable_type.text = f"Type: {variable['type']}"
        self.ids.variable_direction.text = f"Direction: {variable['direction']}"
        self.ids.variable_interval.text = f"Refresh: {variable['interval']}ms"


class MyBaseControllerCard(MDCard):
    def __init__(self, controller: dict):
        super().__init__()
        self.controller: dict = controller
        self.update_view(controller)
        Window.bind(size=self.on_window_resize)

    def update_view(self, controller: dict):
        self.id = controller["name"]
        self.pos = (Window.width * controller["position"][0], Window.height * controller["position"][1])
        self.size = dp(controller["size"][0]), dp(controller["size"][1])
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
    def on_touch_up(self, touch):
        super().on_touch_up(touch)
        if self.collide_point(*touch.pos):
            self.controller["position"] = (self.pos[0] / Window.width, self.pos[1] / Window.height)


class MyButtonControllerEditCard(MyBaseControllerEditCard):
    pass


class MySwitchControllerEditCard(MyBaseControllerEditCard):
    pass


class MySliderControllerEditCard(MyBaseControllerEditCard):
    pass


class MyTextInputControllerEditCard(MyBaseControllerEditCard):
    pass


class MyCreateLayoutDialogContent(MDBoxLayout):
    def __init__(self, layout_name: str = "Default"):
        super().__init__()
        self.ids.layout_name.text = layout_name

    @property
    def edited(self) -> str:
        return self.ids.layout_name.text


class MySelectLayoutDialogContent(MDBoxLayout):
    pass
