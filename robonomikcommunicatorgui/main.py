from kivymd.tools.hotreload.app import MDApp as MDAppHotReload  # Debug only
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
from messenger import Messenger
from session import Session
from saver import Saver
from ui.dialoger import Dialoger
from ui.viewer import Viewer
import ui.styles as styles
import logger
import os


@logger.trace_class
class RobonomikCommunicator(MDAppHotReload):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.messenger: "Messenger" = Messenger()
        self.session: "Session" = Session()
        self.saver: "Saver" = Saver()
        self.viewer: "Viewer" = Viewer()
        self.dialoger: "Dialoger" = Dialoger()
        self.messenger.get_references()
        self.session.get_references()
        self.saver.get_references()
        self.viewer.get_references()
        self.dialoger.get_references()

    def build(self):
        self.kv_path = os.path.abspath("./styles.kv")
        self.title = 'Robonomik Communicator'
        self.theme_cls.material_style = 'M2'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Red'
        self.theme_cls.primary_hue = '800'
        self.theme_cls.accent_palette = 'Orange'
        self.theme_cls.accent_hue = '500'
        Window.size = (1024, 768)
        return Builder.load_file(self.kv_path)

    def on_start(self):
        Clock.schedule_once(lambda *x: self.viewer.open_group_by_type(styles.MyClosedPortViewGroup))
        Clock.schedule_once(lambda *x: self.viewer.open_view_by_type(styles.ConnectWindow))

    def update_kv_file(self, text):
        with open(self.kv_path, "w") as f:
            f.write(text)

    def on_port_select(self, port_name: "str"):
        self.messenger.open(port_name, self.session.default_baudrate)
        self.session.get_current_preset()
        self.viewer.open_group_by_type(styles.MyOpenPortViewGroup)
        self.viewer.open_view_by_type(styles.ConsoleWindow)

    def on_close_port(self):
        self.messenger.close()
        self.viewer.open_group_by_type(styles.MyClosedPortViewGroup)
        self.viewer.open_view_by_type(styles.ConnectWindow)

    def on_ports_list_refresh(self):
        self.viewer.update_current_view()

    def on_message_enter(self, input):
        if input.text == "":
            return
        self.messenger.send(input.text)
        self.viewer.update_current_view()
        input.text = ""

    def on_create_preset(self):
        def create_preset(content: "styles.MyCreatePresetDialog"):
            if self.session.check_if_preset_is_valid(content.edited_preset):
                self.session.set_current_preset(content.edited_preset)
                self.session.save_session()
                self.viewer.update_current_view()
            else:
                self.dialoger.show_text_field_error("preset_name", "Preset name is not valid")
        self.dialoger.show_create_preset_dialog(lambda x: create_preset(x))

    def on_select_preset(self):
        def select_preset(preset_name: "str"):
            self.session.set_current_preset(self.session.get_preset_by_name(preset_name))
            self.viewer.update_current_view()
        self.dialoger.show_select_preset_dialog(lambda x: select_preset(x))

    def on_delete_preset(self):
        def delete_preset():
            self.session.remove_current_preset()
            self.session.save_session()
            self.viewer.update_current_view()
        self.dialoger.show_delete_preset_dialog(lambda x: delete_preset())

    def on_create_variable(self, content: "styles.MyBaseVariableDialog" = None):
        def create_variable(content: "styles.MyBaseVariableDialog"):
            if self.session.check_if_variable_is_valid(content.edited_variable):
                self.session.add_variable(content.edited_variable)
                self.session.save_session()
                self.viewer.update_current_view()
            else:
                self.dialoger.show_text_field_error("variable_name", "Variable name is not valid")
        self.dialoger.show_create_variable_dialog(content, lambda x: create_variable(x))  # Replace this with a separate view

    def on_edit_variable(self, root: "styles.MyVariableCard"):
        def edit_variable(content: "styles.MyBaseVariableDialog"):
            self.session.edit_variable(content.variable, content.edited_variable)
            self.session.save_session()
            self.viewer.update_current_view()
        self.dialoger.show_edit_variable_dialog(root.variable, lambda x: edit_variable(x))  # Replace this with a separate view

    def on_delete_variable(self, root: "styles.MyVariableCard"):
        def delete_variable():
            self.session.remove_variable(root.variable)
            self.session.save_session()
            self.viewer.update_current_view()
        self.dialoger.show_delete_variable_dialog(lambda x: delete_variable())

    def on_create_layout(self):
        def create_layout(content: "styles.MyCreateLayoutDialog"):
            if self.session.check_if_layout_is_valid(content.edited_layout):
                self.session.set_current_layout(content.edited_layout)
                self.session.save_session()
                self.viewer.update_current_view()
            else:
                self.dialoger.show_text_field_error("layout_name", "Layout name is not valid")
        self.dialoger.show_create_layout_dialog(lambda x: create_layout(x))

    def on_edit_layout(self):
        self.session.save_session()
        self.viewer.open_view_by_type(styles.LayoutsEditWindow)

    def on_save_layout(self):
        self.session.save_session()
        self.viewer.open_view_by_type(styles.LayoutsWindow)

    def on_cancel_layout(self):
        self.session.discard_session()
        self.viewer.open_view_by_type(styles.LayoutsWindow)

    def on_select_layout(self):
        def select_layout(layout_name: "str"):
            self.session.set_current_layout(self.session.get_layout_by_name(layout_name))
            self.viewer.update_current_view()
        self.dialoger.show_select_layout_dialog(lambda x: select_layout(x))

    def on_delete_layout(self):
        def delete_layout():
            self.session.remove_current_layout()
            self.session.save_session()
            self.viewer.update_current_view()
        self.dialoger.show_delete_layout_dialog(lambda x: delete_layout())

    def on_add_controller(self):
        self.viewer.open_view_by_type(styles.CreateControllerWindow)

    def on_save_controller(self):
        self.session.save_session()
        self.viewer.open_view_by_type(styles.LayoutsEditWindow)

    def on_cancel_controller(self):
        self.session.discard_session()
        self.viewer.open_view_by_type(styles.LayoutsEditWindow)

    def on_edit_controller(self, root: "styles.MyBaseControllerEditCard"):
        # def edit_controller(content: "styles.MyBaseControllerDialog"):
        #     self.session.edit_controller(content.controller, content.edited_controller)
        #     self.viewer.update_current_view()
        # self.dialoger.show_edit_controller_dialog(root.controller, lambda x: edit_controller(x))  # Replace this with a separate view
        self.viewer.open_view_by_type(styles.CreateControllerWindow)

    def on_delete_controller(self, root: "styles.MyBaseControllerEditCard"):
        def delete_controller():
            self.session.remove_controller(root.controller)
            self.viewer.update_current_view()
        self.dialoger.show_delete_controller_dialog(lambda x: delete_controller())


if __name__ == '__main__':
    app = RobonomikCommunicator()
    app.run()
