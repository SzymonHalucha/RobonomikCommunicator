from __future__ import annotations
from views.desktop.main_desktop_view import MainDesktopView
from views.mobile.main_mobile_view import MainMobileView
from presenters.main_presenter import MainPresenter


data: dict[str, dict[str, type]] = {
    # "Account": {
    #     "desktop": AccountDesktopView,
    #     "tablet": AccountDesktopView,
    #     "mobile": AccountMobileView,
    #     "presenter": AccountPresenter
    # },
    # "Connected": {
    #     "desktop": ConnectedDesktopView,
    #     "tablet": ConnectedDesktopView,
    #     "mobile": ConnectedMobileView,
    #     "presenter": ConnectedPresenter
    # },
    "Main": {
        "mobile": MainMobileView,
        "tablet": MainDesktopView,
        "desktop": MainDesktopView,
        "presenter": MainPresenter
    }
}
