from __future__ import annotations
from kivy.core.window import Window
from kivymd.tools.hotreload.app import MDApp
from views.common.dialoger import Dialoger
from views.common.root import MyRootWidget
from models.messenger import Messenger
from models.session import Session
from models.saver import Saver
import views.views as views
import importlib
import os


class RobonomikCommunicatorHotReload(MDApp):
    KV_DIRS = [os.path.abspath("./views")]

    def build_app(self) -> MyRootWidget:
        importlib.reload(views)
        self.set_application_style()
        self.saver: Saver = Saver()
        self.messenger: Messenger = Messenger()
        self.dialoger: Dialoger = Dialoger()
        self.session: Session = Session()
        self.session.get_references()
        Window.bind(on_key_down=self.on_keyboard_down)
        return self.generate_application_views()

    def set_application_style(self):
        self.title = "Robonomik Communicator DEBUG"
        self.theme_cls.material_style = "M2"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.accent_hue = "500"
        Window.size = (1024, 768)

    def generate_application_views(self) -> MyRootWidget:
        root = MyRootWidget()
        for name in views.data:
            presenter = views.data[name]["presenter"](messenger=self.messenger, session=self.session)
            root.add_desktop_view(name, views.data[name]["desktop"](manager=root, dialoger=self.dialoger, presenter=presenter))
            root.add_tablet_view(name, views.data[name]["tablet"](manager=root, dialoger=self.dialoger, presenter=presenter))
            root.add_mobile_view(name, views.data[name]["mobile"](manager=root, dialoger=self.dialoger, presenter=presenter))
        return root

    def on_keyboard_down(self, window, keyboard, keycode, text, modifiers):
        if "ctrl" in modifiers and text == "r":
            self.rebuild()


class RobonomikCommunicator(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_all_kv_files(os.path.abspath("./views"))
        self.set_application_style()

    def build(self) -> MyRootWidget:
        return self.generate_application_views()

    def set_application_style(self):
        self.title = "Robonomik Communicator"
        self.theme_cls.material_style = "M2"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "800"
        self.theme_cls.accent_palette = "Orange"
        self.theme_cls.accent_hue = "500"
        Window.size = (1024, 768)

    def generate_application_views(self) -> MyRootWidget:
        root = MyRootWidget()
        for name in views.data:
            presenter = views.data[name]["presenter"]()
            root.add_desktop_view(name, presenter.set_desktop_view(views.data[name]["desktop"](presenter=presenter)))
            root.add_tablet_view(name, presenter.set_tablet_view(views.data[name]["tablet"](presenter=presenter)))
            root.add_mobile_view(name, presenter.set_mobile_view(views.data[name]["mobile"](presenter=presenter)))
        return root


if __name__ == '__main__' and __debug__:
    RobonomikCommunicatorHotReload().run()
elif __name__ == '__main__' and not __debug__:
    RobonomikCommunicator().run()
