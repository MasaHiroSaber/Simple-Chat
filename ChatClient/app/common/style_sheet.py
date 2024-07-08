# coding: utf-8
from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    HOME_INTERFACE = "home_interface"
    VIEW_INTERFACE = "view_interface"
    SETTING_INTERFACE = "setting_interface"
    GALLERY_INTERFACE = "gallery_interface"
    NAVIGATION_VIEW_INTERFACE = "navigation_view_interface"
    FRIEND_INTERFACE = "friend_interface"
    CHAT_INTERFACE = 'chat_interface'

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/qss/{theme.value.lower()}/{self.value}.qss"
