from __future__ import annotations
from kivymd.uix.boxlayout import MDBoxLayout as MDBoxLoayout
from views.base_subview import BaseSubview
import presenters.base_presenter as base_presenter
import views.common.root as root
import views.common.dialoger as dialoger


class BaseView(MDBoxLoayout):
    def __init__(self, **kwargs):
        super().__init__()
        self._presenter: base_presenter.BasePresenter = kwargs.get("presenter", None)
        self._manager: root.MyRootWidget = kwargs.get("manager", None)
        self._dialoger: dialoger.Dialoger = kwargs.get("dialoger", None)
        self._subviews: list[BaseSubview] = []
        self._find_all_subviews()

    def open_view_by_name(self, view_name: str):
        self._manager.set_view_by_name(view_name)

    def open_view_by_type(self, view_type: type):
        self._manager.set_view_by_type(view_type)

    def open_subview_by_name(self, subview_name: str, **kwargs):
        [subview.open(**kwargs) if subview.__class__.__name__ == subview_name else subview.close() for subview in self._subviews]
        self.update_current_subview()

    def open_subview_by_type(self, subview_type: type, **kwargs):
        [subview.open(**kwargs) if isinstance(subview, subview_type) else subview.close() for subview in self._subviews]
        self.update_current_subview()

    def close_subviews(self):
        [subview.close() for subview in self._subviews]

    def update_current_subview(self, **kwargs):
        [subview.update(**kwargs) for subview in self._subviews if subview.is_active]

    def get_current_subview(self) -> BaseSubview | None:
        return next(iter(subview for subview in self._subviews if subview.is_active), None)

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
