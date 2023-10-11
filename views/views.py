from __future__ import annotations
from views.desktop.main_desktop_view import MainDesktopView
from views.mobile.main_mobile_view import MainMobileView
from presenters.main_presenter import MainPresenter
from views.desktop.connected_desktop_view import ConnectedDesktopView
from views.mobile.connected_mobile_view import ConnectedMobileView
from presenters.connected_presenter import ConnectedPresenter


data: dict[str, dict[str, type]] = {
    "Main": {
        "mobile": MainMobileView,
        "tablet": MainDesktopView,
        "desktop": MainDesktopView,
        "presenter": MainPresenter
    },
    "Connected": {
        "desktop": ConnectedDesktopView,
        "tablet": ConnectedDesktopView,
        "mobile": ConnectedMobileView,
        "presenter": ConnectedPresenter
    },
    # "Account": {
    #     "desktop": AccountDesktopView,
    #     "tablet": AccountDesktopView,
    #     "mobile": AccountMobileView,
    #     "presenter": AccountPresenter
    # }
}
