from kivy.uix.widget import Widget
from kivymd.app import MDApp
import logger


@logger.trace_class
class View(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_active: "bool" = False
        self.view_name: "str" = self.__class__.__name__
        self._app = MDApp.get_running_app()

    def open(self, parent: "Widget"):
        if self not in parent.children:
            parent.add_widget(self)
        self.is_active = True
        self.update()

    def close(self, parent: "Widget"):
        self.is_active = False
        if self in parent.children:
            parent.remove_widget(self)

    def update(self):
        raise NotImplementedError(f"Method \"update\" is not implemented in class {self.__class__.__name__}")
