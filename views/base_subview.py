from __future__ import annotations
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout


class BaseSubview(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name: str = self.__class__.__name__
        self.view: Widget = None
        self.is_active: bool = False
        self._static_parent: Widget = None

    def open(self, **kwargs):
        if self._static_parent is None:
            self._static_parent = self.parent
        if self not in self._static_parent.children:
            self._static_parent.add_widget(self)
        self.is_active = True
        self.update(**kwargs)

    def close(self):
        if self._static_parent is None:
            self._static_parent = self.parent
        if self in self._static_parent.children:
            self._static_parent.remove_widget(self)
        self.is_active = False

    def update(self, **kwargs):
        raise NotImplementedError(f"Method \"update\" is not implemented in class {self.__class__}")
