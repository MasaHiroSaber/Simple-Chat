from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication
from qfluentwidgets import SplitTitleBar
from qframelesswindow import AcrylicWindow

from ChatClient.app.ui.user_details import Ui_Form


class UserDetailWindow(AcrylicWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.setWindowTitle('User Details')
        self.setWindowIcon(QIcon(":/images/logo.png"))
        self.setFixedSize(400, 600)

        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
