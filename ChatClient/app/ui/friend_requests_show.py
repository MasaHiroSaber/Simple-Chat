import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QApplication, QHBoxLayout, QListWidget, QListWidgetItem
from qfluentwidgets import ScrollArea, SplitTitleBar, SingleDirectionScrollArea, AvatarWidget, StrongBodyLabel, \
    ToolButton, ListWidget
from qframelesswindow import AcrylicWindow
from qfluentwidgets import FluentIcon as FIF
from ChatClient.app.common.style_sheet import StyleSheet
from ChatClient.app.ui.friend_requests import Ui_Form


class FriendRequestWindow(AcrylicWindow):
    on_window_close = pyqtSignal()
    on_accept_request = pyqtSignal(str, str)
    on_reject_request = pyqtSignal(str, str)

    def __init__(self, request):
        super().__init__()
        self.selected_item = None
        self.selected_index = None
        self.view = QWidget()
        self.request = request
        self.reflection = {}

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        StyleSheet.VIEW_INTERFACE.apply(self.view)

        self.setWindowTitle('Friend Request')
        self.setWindowIcon(QIcon(":/images/logo.png"))
        self.setFixedSize(340, 400)

        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False)
        self.vBoxLayout = QVBoxLayout(self)

        self.listWidget = ListWidget()
        self.listWidget.setSelectRightClickedRow(True)
        self.listWidget.setFixedSize(320, 380)
        self.listWidget.itemSelectionChanged.connect(self.on_item_selection_changed)

        self.refreshList()
        self.__initWidgets()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def refreshList(self):
        # 用了个很抽象的部分，用字典来映射列表里的值
        self.listWidget.clear()
        # self.listWidget.setStyleSheet()
        stands = []
        self.reflection = {}
        index = 0
        for request in self.request:
            content = f"来自 {request[1]} 于 {request[3]} 的好友申请"
            stands.append(content)
            self.reflection[str(index)] = request[0]
            index += 1

        for stand in stands:
            item = QListWidgetItem(stand)
            self.listWidget.addItem(item)

    def __initWidgets(self):
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(30, 50, 30, 30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.acceptButton = ToolButton()
        self.acceptButton.setIcon(FIF.ACCEPT)
        self.acceptButton.clicked.connect(self.response_accept)

        self.rejectButton = ToolButton()
        self.rejectButton.setIcon(FIF.CLOSE)
        self.rejectButton.clicked.connect(self.response_reject)

        self.hBoxLayout = QHBoxLayout()
        self.vBoxLayout.addWidget(self.listWidget, 0, Qt.AlignTop)
        self.vBoxLayout.addLayout(self.hBoxLayout, 1)
        self.hBoxLayout.addWidget(self.acceptButton)
        self.hBoxLayout.addWidget(self.rejectButton)

    def on_item_selection_changed(self):
        self.selected_index = self.listWidget.currentRow()
        self.selected_item = self.listWidget.currentItem().text()

    def response_accept(self):
        if self.selected_item is not None:
            fid = self.reflection[str(self.selected_index)]
            self.on_accept_request.emit(str(fid), 'accepted')
            self.deleteEnum(fid)
            self.refreshList()

    def response_reject(self):
        if self.selected_item is not None:
            fid = self.reflection[str(self.selected_index)]
            self.on_reject_request.emit(str(fid), 'rejected')
            self.deleteEnum(fid)
            self.refreshList()

    def deleteEnum(self, fid):
        for i, sublist in enumerate(self.request):
            if sublist[0] == int(fid):
                del self.request[i]
                break

    def closeEvent(self, a0):
        self.on_window_close.emit()
