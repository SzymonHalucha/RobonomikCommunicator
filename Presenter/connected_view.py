from __future__ import annotations
import Presenter.base_presenter as base_presenter

if __debug__:
    import importlib
    import View.ConnectedView
    importlib.reload(View.ConnectedView)


class ConnectedViewPresenter(base_presenter.BasePresenter):
    pass
