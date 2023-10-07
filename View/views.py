from Presenter import MainViewPresenter
from Presenter import ConnectedViewPresenter
from View.MainView import MainView
from View.ConnectedView import ConnectedView

views = {
    "MainView": {
        "presenter": MainViewPresenter,
        "view": MainView
    },
    "ConnectedView": {
        "presenter": ConnectedViewPresenter,
        "view": ConnectedView
    }
}
