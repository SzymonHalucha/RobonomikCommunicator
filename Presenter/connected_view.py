from .base_presenter import BasePresenter

if __debug__:
    import importlib
    import View.ConnectedView
    importlib.reload(View.ConnectedView.connected_view)


class ConnectedViewPresenter(BasePresenter):
    pass
