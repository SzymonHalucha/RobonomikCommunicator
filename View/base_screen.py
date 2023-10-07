from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class BaseScreenView(MDScreen):
    screen_manager = ObjectProperty()
    controller = ObjectProperty()
    model = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._app = MDApp.get_running_app()
        self.model.subscribe(self.on_model_update)

    def on_model_update(self, *args):
        print(f" Model updated: {args}")
