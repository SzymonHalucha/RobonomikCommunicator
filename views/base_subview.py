from __future__ import annotations
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from presenters.base_presenter import BasePresenter
import views.base_view as base_view


class BaseSubview(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name: str = self.__class__.__name__
        self.is_active: bool = True
        self.view: base_view.BaseView = None
        self.presenter: BasePresenter = None
        self._static_parent: Widget = None

    def open(self):
        if not self.is_active:
            if self._static_parent is None:
                self._static_parent = self.parent
            if self not in self._static_parent.children:
                self._static_parent.add_widget(self)
        self.is_active = True
        self.update()

    def close(self):
        if self.is_active:
            if self._static_parent is None:
                self._static_parent = self.parent
            if self in self._static_parent.children:
                self._static_parent.remove_widget(self)
        self.is_active = False

    def update(self):
        if not self.is_active:
            return

    def get_tab_title(self) -> str:
        return self._static_parent.title

    def copy_from(self, other: BaseSubview) -> BaseSubview:
        self.name = other.name
        self.view = other.view
        self.presenter = other.presenter
        self.is_active = other.is_active
        self._static_parent = other._static_parent if other._static_parent is not None else other.parent
        return self
