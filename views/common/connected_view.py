from __future__ import annotations
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from views.base_view import BaseView
from views.base_subview import BaseSubview
import presenters.connected_presenter as connected_presenter
import views.common.common as common


class ConnectedView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = kwargs.get("presenter", None)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.open_subview_by_name(f"{tab_text}Subview")

    def on_message_send(self, instance: MDTextField):
        def on_send(*args):
            instance.text = ""
            self.get_current_subview().update_console(args)
        self.presenter.on_message_send(instance.text, on_send)

    def on_variable_create(self):
        print("on_variable_create")


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

    def update(self):
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
        pass


class LayoutsEditSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = self.presenter

    def update(self):
        pass


class VariablesSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = self.presenter

    def update(self):
        self.update_variables_list(self.presenter.get_variables())

    def update_variables_list(self, variables: list[tuple[str, str, str, int]]):
        items = [item for item in self.ids.variables_list.children if isinstance(item, MyVariableCard)]
        names = [item.name for item in items]
        [self.ids.variables_list.remove_widget(items[i]) if var[0] not in names else items[i].update_view(var) for i, var in enumerate(variables)]
        [self.ids.variables_list.add_widget(MyVariableCard(var)) for var in variables if var[0] not in names]


class MyVariableCard(MDCard):
    def __init__(self, variable: tuple[str, str, str, int]):
        super().__init__()
        self.name: str = variable[0]
        self.update_view(variable)

    def update_view(self, variable: tuple[str, str, str, int]):
        self.id = self.name
        self.ids.variable_name.text = f"Name: {variable[0]}"
        self.ids.variable_type.text = f"Type: {variable[1]}"
        self.ids.variable_direction.text = f"Direction: {variable[2]}"
        self.ids.variable_interval.text = f"Refresh: {variable[3]}ms"


# class MyBaseVariableDialog(MDBoxLayout):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args)
#         self.next_type: "MyBaseVariableDialog" = None
#         self.variable: "Variable" = kwargs["variable"] if "variable" in kwargs else None
#         if self.variable is not None:
#             self.ids.variable_name.text = self.variable.name
#             self.ids.variable_type.text = self.variable.type
#             self.ids.variable_direction.text = self.variable.direction
#             self.ids.variable_interval.text = str(self.variable.interval)

#     @property
#     def edited_variable(self) -> "Variable":
#         return Variable(name=self.ids.variable_name.text,
#                         type=self.ids.variable_type.text,
#                         direction=self.ids.variable_direction.text,
#                         interval=int(self.ids.variable_interval.text if "variable_interval" in self.ids else "0"))

#     def on_variable_direction_click(self):
#         self.ids.variable_direction.text = "Input" if self.ids.variable_direction.text == "Output" else "Output"

#     def on_variable_type_click(self):
#         MDApp.get_running_app().on_create_variable(self.next_type())


# class MyTriggerVariableDialog(MyBaseVariableDialog):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.next_type: "MyBaseVariableDialog" = MyIntVariableDialog
#         self.ids.variable_type.text = "Trigger"


# class MyIntVariableDialog(MyBaseVariableDialog):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.next_type: "MyBaseVariableDialog" = MyFloatVariableDialog
#         self.ids.variable_type.text = "Int"


# class MyFloatVariableDialog(MyBaseVariableDialog):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.next_type: "MyBaseVariableDialog" = MyStringVariableDialog
#         self.ids.variable_type.text = "Float"


# class MyStringVariableDialog(MyBaseVariableDialog):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.next_type: "MyBaseVariableDialog" = MyTriggerVariableDialog
#         self.ids.variable_type.text = "String"
