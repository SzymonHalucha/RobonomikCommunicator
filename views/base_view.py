from __future__ import annotations
from kivymd.uix.boxlayout import MDBoxLayout as MDBoxLoayout
from views.base_subview import BaseSubview
import presenters.base_presenter as base_presenter


class BaseView(MDBoxLoayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.presenter: base_presenter.BasePresenter = None
        self._subviews: list[BaseSubview] = []
        self._find_all_subviews()

    def open_subview_by_name(self, subview_name: str):
        [subview.open() if subview.__class__.__name__ == subview_name else subview.close() for subview in self._subviews]

    def open_subview_by_type(self, subview_type: type):
        [subview.open() if isinstance(subview, subview_type) else subview.close() for subview in self._subviews]

    def close_subviews(self):
        [subview.close() for subview in self._subviews]

    def update_current_subview(self):
        [subview.update() for subview in self._subviews if subview.is_active]

    def _find_all_subviews(self):
        def find(root):
            for child in root.children:
                if isinstance(child, BaseSubview):
                    self._subviews.append(child)
                    child.view = self
                find(child)
        find(self)
        if len(self._subviews) > 0:
            [subview.close() for subview in self._subviews]
