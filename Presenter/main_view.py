from .base_presenter import BasePresenter

if __debug__:
    import importlib
    import View.MainView
    importlib.reload(View.MainView.main_view)


class MainViewPresenter(BasePresenter):
    pass
