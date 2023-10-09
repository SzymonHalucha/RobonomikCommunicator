from __future__ import annotations
from views.base_view import BaseView


class ConnectedDesktopView(BaseView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
