from __future__ import annotations
import Presenter.main_view as main_view_presenter
import Presenter.connected_view as connected_view_presenter
import View.MainView.main_view as main_view
import View.ConnectedView.connected_view as connected_view

views_dict: dict = {
    "MainView": {
        "presenter": main_view_presenter.MainViewPresenter,
        "view": main_view.MainView
    },
    "ConnectedView": {
        "presenter": connected_view_presenter.ConnectedViewPresenter,
        "view": connected_view.ConnectedView
    }
}
