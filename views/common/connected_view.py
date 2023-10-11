from __future__ import annotations
from views.base_view import BaseView
from views.base_subview import BaseSubview
import presenters.connected_presenter as connected_presenter
import views.common.common as common


class ConnectedView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.presenter: connected_presenter.ConnectedPresenter = kwargs.get("presenter", None)

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        self.open_subview_by_name(f"{tab_text}Subview")
