from __future__ import annotations
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
import presenters.base_presenter as base_presenter


class BaseView(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: base_presenter.BasePresenter = None
        self.screen_manager: MDScreenManager = None
