from kivymd.uix.list import IRightBodyTouch, BaseListItem, TwoLineRightIconListItem, TwoLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsBase


class DesktopView(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MyTab(MDFloatLayout, MDTabsBase):
    pass


class ConnectWindow(MDBoxLayout):
    pass


class SettingsWindow(MDBoxLayout):
    pass


class MyListItemWithCheckbox(BaseListItem):
    pass


class MyRightCheckboxContainer(IRightBodyTouch, MDCheckbox):
    pass


class MyTwoLineListItemWithCheckbox(TwoLineRightIconListItem, MyListItemWithCheckbox):
    pass


class MyTwoLineAvatarIconListItem(TwoLineAvatarIconListItem):
    pass
