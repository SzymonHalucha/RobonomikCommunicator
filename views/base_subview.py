from __future__ import annotations
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from presenters.base_presenter import BasePresenter
import views.base_view as base_view


class BaseSubview(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name: str = self.__class__.__name__
        self.view: base_view.BaseView = None
        self.presenter: BasePresenter = None
        self.is_active: bool = False
        self._static_parent: Widget = None

    def open(self):
        if self._static_parent is None:
            self._static_parent = self.parent
        if self not in self._static_parent.children:
            self._static_parent.add_widget(self)
        self.is_active = True
        self.update()

    def close(self):
        if self._static_parent is None:
            self._static_parent = self.parent
        if self in self._static_parent.children:
            self._static_parent.remove_widget(self)
        self.is_active = False

    def update(self):
        raise NotImplementedError(f"Method \"update\" is not implemented in class {self.__class__}")

    def copy_from(self, other: BaseSubview) -> BaseSubview:
        self.name = other.name
        self.view = other.view
        self.presenter = other.presenter
        self.is_active = other.is_active
        self._static_parent = other._static_parent if other._static_parent is not None else other.parent
        return self
