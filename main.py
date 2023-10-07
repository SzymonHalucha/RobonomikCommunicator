from View import views
from View import BaseView
from Model.database import Database
from Presenter.base_presenter import BasePresenter
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.tools.hotreload.app import MDApp
from kivy.core.window import Window
from kivy.clock import Clock
import os


class RobonomikCommunicatorHotReload(MDApp):
    KV_DIRS = [os.path.abspath("./View")]

    def build_app(self) -> "MDScreenManager":
        import importlib
        import View.views
        importlib.reload(View.views)
        self.screen_manager = MDScreenManager()
        self.database = Database()
        self.set_application_style()
        self.generate_application_views()
        Window.bind(on_key_down=self.on_keyboard_down)
        return self.screen_manager

    def set_application_style(self):
        self.title = "Robonomik Communicator DEBUG"
        self.theme_cls.material_style = "M2"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.accent_hue = "500"
        Window.size = (1024, 768)

    def generate_application_views(self, *args):
        for i, view_name in enumerate(views.views.keys()):
            view: "BaseView" = views.views[view_name]["view"](name=view_name)
            presenter: "BasePresenter" = views.views[view_name]["presenter"]()
            presenter.view = view
            view.presenter = presenter
            view.screen_manager = self.screen_manager
            self.screen_manager.add_widget(view)

    def on_keyboard_down(self, window, keyboard, keycode, text, modifiers):
        if "ctrl" in modifiers and text == "r":
            self.rebuild()


class RobonomikCommunicator(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(os.path.abspath("./View"))
        self.screen_manager = MDScreenManager()
        self.database = Database()

    def build(self) -> "MDScreenManager":
        self.set_application_style()
        self.generate_application_views()
        return self.screen_manager

    def set_application_style(self):
        self.title = "Robonomik Communicator"
        self.theme_cls.material_style = "M2"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.accent_hue = "500"
        Window.size = (1024, 768)

    def generate_application_views(self, *args):
        for i, view_name in enumerate(views.views.keys()):
            view: "BaseView" = views.views[view_name]["view"](name=view_name)
            presenter: "BasePresenter" = views.views[view_name]["presenter"]()
            presenter.view = view
            view.presenter = presenter
            view.screen_manager = self.screen_manager
            self.screen_manager.add_widget(view)


if __name__ == "__main__":
    if __debug__:
        app = RobonomikCommunicatorHotReload()
    else:
        app = RobonomikCommunicator()
    app.run()
