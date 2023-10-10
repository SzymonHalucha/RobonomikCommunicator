from __future__ import annotations
from kivymd.uix.list import BaseListItem, TwoLineRightIconListItem, TwoLineAvatarIconListItem, IRightBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.tab import MDTabsBase


class MyTab(MDFloatLayout, MDTabsBase):
    pass


class MyTwoLineAvatarIconListItem(TwoLineAvatarIconListItem):
    pass


class MyListItemWithCheckbox(BaseListItem):
    pass


class MyRightCheckboxContainer(IRightBodyTouch, MDCheckbox):
    pass


class MyTwoLineListItemWithCheckbox(TwoLineRightIconListItem, MyListItemWithCheckbox):
    pass
