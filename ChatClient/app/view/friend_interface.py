from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QScrollArea
from qfluentwidgets import ScrollArea, SearchLineEdit

from ChatClient.app.common.style_sheet import StyleSheet


class FriendInterface(ScrollArea):
    def __init__(self, parent=None, username=None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidgets__()

    def __initWidgets__(self):
        self.view.setObjectName('view')
        self.setObjectName('friendInterface')
        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.userSearchEdit = SearchLineEdit(self)
        self.userSearchEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
        self.vBoxLayout.addWidget(self.userSearchEdit)

        StyleSheet.HOME_INTERFACE.apply(self)
        QScrollArea.setStyleSheet(self, 'background-color: transparent')
    def resizeEvent(self, e):
        super().resizeEvent(e)
