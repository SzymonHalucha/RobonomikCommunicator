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
        self.is_active: bool = kwargs.get("is_active", True)
        self.presenter: BasePresenter = kwargs.get("presenter", None)
        self._root: root.MyRootWidget = kwargs.get("root", None)
        self._dialoger: Dialoger = kwargs.get("dialoger", None)
        self._subviews: list[BaseSubview] = []
        self._current: BaseSubview = None
        self._tabs: MDTabs = None
        self._find_all_subviews()

    def open(self, **kwargs):
        if "subview_type" in kwargs and kwargs["subview_type"] is not None:
            self.open_subview_by_type(kwargs["subview_type"])
        elif "subview_name" in kwargs and kwargs["subview_name"] is not None:
            self.open_subview_by_name(kwargs["subview_name"])
        else:
            self.open_subview_by_name(self._subviews[0].name)
        self.is_active = True

    def close(self, **kwargs):
        if self.is_active:
            if kwargs.get("close_subviews", False):
                [subview.close() for subview in self._subviews]
        self.is_active = False

    def open_subview_by_name(self, subview_name: str):
        [self._open_subview(subview) if subview.name == subview_name else subview.close() for subview in self._subviews]

    def open_subview_by_type(self, subview_type: type):
        [self._open_subview(subview)
         if isinstance(subview, subview_type) or issubclass(subview_type, type(subview))
         else subview.close() for subview in self._subviews]

    def update_current_subview(self, *args):
        if self._current is not None:
            self._current.update()

    def get_current_subview(self) -> BaseSubview | None:
        return self._current

    def _open_subview(self, subview: BaseSubview):
        if self._current is not None:
            self._current.close()
        duration = self._tabs.anim_duration
        self._tabs.anim_duration = 0
        self._tabs.switch_tab(subview.get_tab_title(), search_by="title")
        self._tabs.anim_duration = duration
        self._current = subview
        subview.open()

    def _find_all_subviews(self):
        def init_tabs(tabs: MDTabs):
            self._tabs = tabs
            [find(tab) for tab in tabs.get_slides()]

        def find(root):
            for child in root.children:
                init_tabs(child) if isinstance(child, MDTabs) else find(child)
                if issubclass(type(child), BaseSubview):
                    child.view = self
                    child.presenter = self.presenter
                    self._subviews.append(child)
        find(self)
        self._replace_all_subviews()

    def _replace_all_subviews(self):
        all = inspect.getmembers(sys.modules[self.__module__], inspect.isclass)
        classes = [cls for cls in all if not any([isinstance(subview, cls[1]) for subview in self._subviews]) and issubclass(cls[1], BaseSubview)]
        [[self._replace_subview(subview, cls[1]()) for cls in classes if issubclass(cls[1], type(subview))] for subview in self._subviews]

    def _replace_subview(self, old: BaseSubview, new: BaseSubview):
        self._subviews[self._subviews.index(old)] = new.copy_from(old)
        old.parent.remove_widget(old)
