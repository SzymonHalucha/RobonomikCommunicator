from __future__ import annotations
from kivy.core.window import Window
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import BaseButton
from views.base_subview import BaseSubview
from views.base_view import BaseView
import presenters.connected_presenter as connected_presenter
import views.common.common as common
import views.common.main_view as main_view
import sys


class ConnectedView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = kwargs.get("presenter", None)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.open_subview_by_name(f"{tab_text}Subview")

    def on_close_port(self):
        self.presenter.on_close_port()
        self._root.open_view_by_type(main_view.MainView)

    def on_message_send(self, instance: MDTextField):
        def on_send(*args):
            instance.text = ""
            subview = self.get_current_subview()
            if subview is not None:
                subview.update_console(args)
        self.presenter.on_message_send(instance.text, on_send)

    def on_layout_create(self):
        def on_create(content):
            self.presenter.on_layout_create(content.layout, lambda success: self._dialoger.close_dialogs() if success else
                                            self._dialoger.show_name_error("layout_name", "Layout"))
            self.update_current_subview()
        self._dialoger.open_confirm_dialog("Create Layout", common.MyCreateLayoutDialogContent(), on_create)

    def on_layout_select(self):
        self._dialoger.open_list_dialog("Select Layout", self.presenter.on_layout_select(self.update_current_subview))

    def on_layout_edit(self):
        self.open_subview_by_type(LayoutsEditSubview)

    def on_layout_save(self):
        self.presenter.on_layout_save()
        self.open_subview_by_type(LayoutsSubview)

    def on_layout_cancel(self):
        self.presenter.on_layout_cancel()
        self.open_subview_by_type(LayoutsSubview)

    def on_layout_delete(self):
        def on_delete(*args):
            self.presenter.on_layout_delete()
            self._dialoger.close_dialogs()
            self.update_current_subview()
        self._dialoger.open_delete_dialog("Delete Layout", "Are you sure you want to delete this layout?", on_delete)

    def on_controller_add(self):
        self.open_subview_by_type(ControllerCreateSubview)

    # TODO: Change to dropdown menu
    def on_controller_type_click(self, instance: BaseButton):
        if instance.text == "Button":
            instance.text = "Switch"
        elif instance.text == "Switch":
            instance.text = "Slider"
        elif instance.text == "Slider":
            instance.text = "Text Input"
        else:
            instance.text = "Button"

    # TODO: Change to dropdown menu
    def on_controller_direction_click(self, instance: BaseButton):
        if instance.text == "Input":
            instance.text = "Output"
        else:
            instance.text = "Input"

    def on_controller_move(self, id: str, postion: tuple[float, float]):
        self.presenter.on_controller_move(id, postion)

    def on_controller_edit(self, instance: common.MyBaseControllerCard):
        self.open_subview_by_type(ControllerCreateSubview)
        subview = self.get_current_subview()
        if subview is not None:
            subview.set_values(instance.controller)

    def on_controller_save(self, instance: ControllerCreateSubview):
        self.presenter.on_controller_save(instance.controller, lambda success: self.open_subview_by_type(LayoutsEditSubview)
                                          if success else instance.show_error())

    def on_controller_edit_save(self, instance: ControllerCreateSubview):
        self.presenter.on_controller_edit_save(instance.controller, lambda success: self.open_subview_by_type(LayoutsEditSubview)
                                               if success else instance.show_error())

    def on_controller_cancel(self):
        self.open_subview_by_type(LayoutsEditSubview)

    def on_controller_delete(self, instance: common.MyBaseControllerCard):
        def on_delete(*args):
            self._dialoger.close_dialogs()
            self.presenter.on_controller_delete(instance.controller["id"])
            self.update_current_subview()
        self._dialoger.open_delete_dialog("Delete Controller", "Are you sure you want to delete this controller?", on_delete)

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

    def on_variable_edit(self, instance: common.MyVariableCard):
        self.open_subview_by_type(VariableCreateSubview)
        subview = self.get_current_subview()
        if subview is not None:
            subview.set_values(instance.variable)

    def on_variable_save(self, instance: VariableCreateSubview):
        self.presenter.on_variable_save(instance.variable, lambda success: self.open_subview_by_type(VariablesSubview)
                                        if success else instance.show_error())

    def on_variable_edit_save(self, instance: VariableCreateSubview):
        self.presenter.on_variable_edit_save(instance.variable, lambda success: self.open_subview_by_type(VariablesSubview)
                                             if success else instance.show_error())

    def on_variable_cancel(self):
        self.open_subview_by_type(VariablesSubview)

    def on_variable_delete(self, instance: common.MyVariableCard):
        def on_delete(*args):
            self._dialoger.close_dialogs()
            self.presenter.on_variable_delete(instance.variable["id"])
            self.update_current_subview()
        self._dialoger.open_delete_dialog("Delete Variable", "Are you sure you want to delete this variable?", on_delete)


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
        self.update_layout_board(self.presenter.get_current_layout())

    def update_layout_board(self, layout: dict):
        self.ids.layout_name.text = f"Layout: {layout['name']}"
        self.ids.controllers_board.clear_widgets()
        for controller in layout["controllers"]:
            class_name = f"My{controller['type'].replace(' ', '')}ControllerCard"
            self.ids.controllers_board.add_widget(getattr(common, class_name)(controller=controller))


class LayoutsEditSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = self.presenter

    def update(self):
        self.update_layout_board(self.presenter.get_current_layout())

    def update_layout_board(self, layout: dict):
        self.ids.layout_name.text = f"Edit Layout: {layout['name']}"
        self.ids.controllers_board.clear_widgets()
        for controller in layout["controllers"]:
            class_name = f"My{controller['type'].replace(' ', '')}ControllerEditCard"
            self.ids.controllers_board.add_widget(getattr(common, class_name)(controller=controller, view=self.view))


class ControllerCreateSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = self.presenter

    def open(self):
        super().open()
        self.id = ""
        self.ids.controller_name.error = False
        self.ids.controller_name.helper_text = ""
        self.ids.controller_save.on_release = lambda *x: self.view.on_controller_save(self)

    def update(self):
        pass

    def show_error(self):
        self.ids.controller_name.helper_text = "Controller name already exists or is invalid"
        self.ids.controller_name.error = True

    def set_values(self, values: dict):
        self.id = values["id"]
        self.ids.controller_save.on_release = lambda *x: self.view.on_controller_edit_save(self)
        self.ids.controller_name.text = values["name"]
        self.ids.controller_variable.text = values['variable_name']
        self.ids.controller_custom_name.text = values['custom_name']
        self.ids.controller_type.text = values["type"]
        self.ids.controller_min_range.text = str(values["range"][0])
        self.ids.controller_max_range.text = str(values["range"][1])
        self.ids.controller_width.text = str(values["size"][0])
        self.ids.controller_height.text = str(values["size"][1])

    @property
    def controller(self) -> dict:
        return {"id": self.id, "name": self.ids.controller_name.text, "variable_name": self.ids.controller_variable.text,
                "custom_name": self.ids.controller_custom_name.text, "type": self.ids.controller_type.text,
                "range": (float(self.ids.controller_min_range.text), float(self.ids.controller_max_range.text)),
                "position": (float(self.pos[0] / Window.width), float(self.pos[1] / Window.height)),
                "size": (int(self.ids.controller_width.text), int(self.ids.controller_height.text))}


class VariablesSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = self.presenter

    def update(self):
        self.update_variables_list(self.presenter.get_variables())

    def update_variables_list(self, variables: list[dict]):
        self.ids.variables_list.clear_widgets()
        [self.ids.variables_list.add_widget(common.MyVariableCard(view=self.view, variable=var)) for var in variables]


class VariableCreateSubview(BaseSubview):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = self.presenter

    def open(self):
        super().open()
        self.id = ""
        self.ids.variable_name.error = False
        self.ids.variable_name.helper_text = ""
        self.ids.variable_save.on_release = lambda *x: self.view.on_variable_save(self)

    def update(self):
        pass

    def show_error(self):
        self.ids.variable_name.helper_text = "Variable name already exists or is invalid"
        self.ids.variable_name.error = True

    def set_values(self, values: dict):
        self.id = values["id"]
        self.ids.variable_save.on_release = lambda *x: self.view.on_variable_edit_save(self)
        self.ids.variable_name.text = values["name"]
        self.ids.variable_type.text = values["type"]
        self.ids.variable_direction.text = values["direction"]
        self.ids.variable_interval.text = str(values["interval"])

    @property
    def variable(self) -> dict:
        return {"id": self.id, "name": self.ids.variable_name.text, "type": self.ids.variable_type.text,
                "direction": self.ids.variable_direction.text, "interval": int(self.ids.variable_interval.text)}
