from PyQt5.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition


def info_bar(barType, parent, title, content, orient=Qt.Horizontal, isClosable=True, position=InfoBarPosition.TOP_RIGHT,
             duration=2000):
    barType(
        title=title,
        content=content,
        orient=orient,
        isClosable=isClosable,
        position=position,
        duration=duration,
        parent=parent
    )
