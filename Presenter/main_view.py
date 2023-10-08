from __future__ import annotations
import Presenter.base_presenter as base_presenter

if __debug__:
    import importlib
    import View.MainView
    importlib.reload(View.MainView)


class MainViewPresenter(base_presenter.BasePresenter):
    pass
