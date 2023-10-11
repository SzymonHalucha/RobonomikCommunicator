from __future__ import annotations
from kivymd.uix.tab import MDTabs
from kivymd.uix.boxlayout import MDBoxLayout
from presenters.base_presenter import BasePresenter
from views.base_subview import BaseSubview
from views.dialoger import Dialoger
import views.root as root
import inspect
import sys


class BaseView(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = kwargs.get("name", "Default")
        self.is_active: bool = kwargs.get("is_active", False)
        self.presenter: BasePresenter = kwargs.get("presenter", None)
        self._root: root.MyRootWidget = kwargs.get("root", None)
        self._dialoger: Dialoger = kwargs.get("dialoger", None)
        self._subviews: list[BaseSubview] = []
        self._find_all_subviews()

    def open(self):
        if len(self._subviews) > 0 and not any(subview.is_active for subview in self._subviews):
            self._subviews[0].open()
        self.is_active = True

    def close(self):
        [subview.close() for subview in self._subviews]
        self.is_active = False

    def open_subview_by_name(self, subview_name: str):
        [subview.open() if subview.name == subview_name else subview.close() for subview in self._subviews]

    def open_subview_by_type(self, subview_type: type):
        [subview.open() if isinstance(subview, subview_type) or issubclass(subview_type, type(subview)) else subview.close() for subview in self._subviews]

    def update_current_subview(self):
        [subview.update() for subview in self._subviews if subview.is_active]

    def get_current_subview(self) -> BaseSubview | None:
        return next((subview for subview in self._subviews if subview.is_active), None)

    def _find_all_subviews(self):
        def find(root):
            for child in root.children:
                [find(tab) for tab in child.get_slides()] if isinstance(child, MDTabs) else find(child)
                if issubclass(type(child), BaseSubview):
                    child.view = self
                    child.presenter = self.presenter
                    self._subviews.append(child)
        find(self)
        self.close()
        self._replace_all_subviews()

    def _replace_all_subviews(self):
        all = inspect.getmembers(sys.modules[self.__module__], inspect.isclass)
        classes = [cls for cls in all if not any([isinstance(subview, cls[1]) for subview in self._subviews]) and issubclass(cls[1], BaseSubview)]
        [[self._replace_subview(subview, cls[1]()) for cls in classes if issubclass(cls[1], type(subview))] for subview in self._subviews]

    def _replace_subview(self, old: BaseSubview, new: BaseSubview):
        self._subviews[self._subviews.index(old)] = new.copy_from(old)
