from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp


class BaseView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter = None
        self.screen_manager: "MDScreenManager" = None
        self._name: "str" = kwargs.get("name", "BaseView")
        self._app = MDApp.get_running_app()
