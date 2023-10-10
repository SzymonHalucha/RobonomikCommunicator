from __future__ import annotations
from kivy.uix.widget import Widget


class BaseSubview(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_active: bool = False
        self.static_parent: Widget = None
        self.view: Widget = None

    def open(self):
        if self.static_parent is None:
            self.static_parent = self.parent
        if self not in self.static_parent.children:
            self.static_parent.add_widget(self)
        self.is_active = True
        self.update()

    def close(self):
        if self.static_parent is None:
            self.static_parent = self.parent
        if self in self.static_parent.children:
            self.static_parent.remove_widget(self)
        self.is_active = False

    def update(self):
        pass
        # raise NotImplementedError(f"Method \"update\" is not implemented in class {self.__class__}")
