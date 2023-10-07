from View.screens import screens
from Model.database import Database
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.tools.hotreload.app import MDApp
from kivy.core.window import Window


class RobonomikCommunicatorHotReload(MDApp):
    def build_app(self) -> "MDScreenManager":
        import importlib
        import View.screens
        importlib.reload(View.screens)
        self.screen_manager = MDScreenManager()
        self.database = Database()
        Window.bind(on_key_down=self.on_keyboard_down)
        self.generate_application_screens()
        return self.screen_manager

    def on_keyboard_down(self, window, keyboard, keycode, text, modifiers):
        if "ctrl" in modifiers and text == "r":
            self.rebuild()

    def generate_application_screens(self):
        for i, screen_name in enumerate(screens.keys()):
            model = screens[screen_name]["model"](self.database)
            controller = screens[screen_name]["controller"](model)
            view = controller.get_view()
            view.name = screen_name
            view.screen_manager = self.screen_manager
            self.screen_manager.add_widget(view)


class RobonomikCommunicator(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(self.directory)
        self.screen_manager = MDScreenManager()
        self.database = Database()

    def build(self) -> "MDScreenManager":
        self.generate_application_screens()
        return self.screen_manager

    def generate_application_screens(self):
        for i, screen_name in enumerate(screens.keys()):
            model = screens[screen_name]["model"](self.database)
            controller = screens[screen_name]["controller"](model)
            view = controller.get_view()
            view.name = screen_name
            view.screen_manager = self.screen_manager
            self.screen_manager.add_widget(view)


if __name__ == "__main__":
    if __debug__:
        app = RobonomikCommunicatorHotReload()
    else:
        app = RobonomikCommunicator()
    app.run()
