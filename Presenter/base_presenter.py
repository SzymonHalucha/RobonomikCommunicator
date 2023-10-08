from __future__ import annotations
import View.base_view as base_view


class BasePresenter:
    def __init__(self):
        self.view: base_view.BaseView = None
