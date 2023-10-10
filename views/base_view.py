from __future__ import annotations
from kivymd.uix.boxlayout import MDBoxLayout
from presenters.base_presenter import BasePresenter
from views.base_subview import BaseSubview
from views.dialoger import Dialoger


class BaseView(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = kwargs.get("name", "Default")
        self.is_active: bool = kwargs.get("is_active", False)
        self.presenter: BasePresenter = kwargs.get("presenter", None)
        self._dialoger: Dialoger = kwargs.get("dialoger", None)
        self._subviews: list[BaseSubview] = []
        self._find_all_subviews()

    def open(self, **kwargs):
        if len(self._subviews) > 0 and not any(subview.is_active for subview in self._subviews):
            self._subviews[0].open(**kwargs)
        self.is_active = True

    def close(self):
        [subview.close() for subview in self._subviews]
        self.is_active = False

    def open_subview_by_name(self, subview_name: str, **kwargs):
        [subview.open(**kwargs) if subview.name == subview_name else subview.close() for subview in self._subviews]

    def open_subview_by_type(self, subview_type: type, **kwargs):
        [subview.open(**kwargs) if isinstance(subview, subview_type) else subview.close() for subview in self._subviews]

    def update_current_subview(self, **kwargs):
        [subview.update(**kwargs) for subview in self._subviews if subview.is_active]

    def _find_all_subviews(self, *args):
        def find(root):
            for child in root.children:
                find(child)
                if isinstance(child, BaseSubview):
                    self._subviews.append(child)
                    child.view = self
        find(self)
        self.close()
