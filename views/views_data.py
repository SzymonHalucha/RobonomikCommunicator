from __future__ import annotations
import views.main_view.main_view as main_view
import views.connected_view.connected_view as connected_view
import presenters.connected_presenter as connected_presenter
import presenters.main_presenter as main_presenter

data: dict = {
    "Main": {
        "view": main_view.MainView,
        "presenter": main_presenter.MainPresenter
    },
    "Connected": {
        "view": connected_view.ConnectedView,
        "presenter": connected_presenter.ConnectedPresenter
    }
}
