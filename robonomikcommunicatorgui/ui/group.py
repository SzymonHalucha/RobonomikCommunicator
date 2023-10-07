from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.app import MDApp
from kivy.clock import Clock
from ui.view import View
import logger


@logger.trace_class
class Group(MDTabs):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_active: "bool" = False
        self.group_name: "str" = self.__class__.__name__
        self._views: "dict[MDTabsBase, list[View]]" = {}
        self._app = MDApp.get_running_app()
        self._app.viewer.register_group(self)
        Clock.schedule_once(self.on_all_created)

    def __del__(self):
        if self._app is not None and self._app.viewer is not None:
            self._app.viewer.unregister_group(self)

    def open(self):
        self.is_active = True
        if self._app.root is not None and self not in self._app.root.children:
            self._app.root.add_widget(self)

    def close(self):
        self.is_active = False
        if self._app.root is not None and self in self._app.root.children:
            self._app.root.remove_widget(self)
        [view.close(tab) for tab in self._views for view in self._views[tab]]
        self.switch_tab(list(self._views.keys())[0].title)

    def open_view_by_type(self, view_type: "type"):
        if self.is_active:
            [[view.open(tab) if isinstance(view, view_type) else view.close(tab) for view in self._views[tab]] for tab in self._views]

    def update_opened_views(self):
        if self.is_active:
            [[view.update() for view in self._views[tab] if view.is_active] for tab in self._views]

    def on_all_created(self, *args):
        for tab in self.get_slides():
            self._views[tab] = [child for child in tab.children if isinstance(child, View)]

    def on_tab_switch(self, instance_tabs, instance_tab, tab_text):
        if self.is_active:
            [self._views[tb][-1].open(tb) for tb in self._views if tb.tab_label_text == tab_text and not any(view.is_active for view in self._views[tb])]
