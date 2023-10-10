from __future__ import annotations
from views.common.main_view import MainDesktopView, MainMobileView
# from views.desktop.main_desktop_view import MainDesktopView
# from views.desktop.account_desktop_view import AccountDesktopView
# from views.desktop.connected_desktop_view import ConnectedDesktopView
# from views.mobile.main_mobile_view import MainMobileView
# from views.mobile.account_mobile_view import AccountMobileView
# from views.mobile.connected_mobile_view import ConnectedMobileView
from presenters.main_presenter import MainPresenter
# from presenters.account_presenter import AccountPresenter
# from presenters.connected_presenter import ConnectedPresenter


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
