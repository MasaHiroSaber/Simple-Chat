from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication
from qfluentwidgets import SplitTitleBar
from qframelesswindow import AcrylicWindow

from ChatClient.app.ui.user_details import Ui_Form


class UserDetailWindow(AcrylicWindow, Ui_Form):
    on_add_friend = pyqtSignal(str)
    on_send_message = pyqtSignal(str)

    def __init__(self, selectUserName):
        super().__init__()
        self.setupUi(self)

        self.setTitleBar(SplitTitleBar(self))
        self.selectUserName = selectUserName
        self.titleBar.raise_()
        self.addFriend = False
        self.sendMessage = False

        self.setWindowTitle('User Details')
        self.setWindowIcon(QIcon(":/images/logo.png"))
        self.setFixedSize(300, 450)

        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False)

        self.function_button.clicked.connect(self.function_button_clicked)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def function_button_clicked(self):
        if self.addFriend:
            self.on_add_friend.emit(self.selectUserName)

        elif self.sendMessage:
            self.on_send_message.emit(self.selectUserName)
