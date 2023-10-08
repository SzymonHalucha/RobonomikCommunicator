from __future__ import annotations
import views.base_view as base_view


class BasePresenter:
    def __init__(self):
        self.view: base_view.BaseView = None
