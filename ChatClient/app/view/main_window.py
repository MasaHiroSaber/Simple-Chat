import sys

from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF
# from ChatClient.app.common.signal_bus import signalBus

from ChatClient.app.view.home_interface import HomeInterface
from ChatClient.app.view.friend_interface import FriendInterface
from ChatClient.app.view.chat_interface import ChatInterface


class MainWindow(FluentWindow):
    """主窗口类，继承自FluentWindow"""
    def __init__(self, client, username=None):
        """初始化主窗口"""
        super().__init__()
        self.initWindow()

        self.client = client
        self.username = username
        self.userFriends = None
        self.homeInterface = HomeInterface(self.client, self, self.username)
        self.friendInterface = FriendInterface(self.client, self, self.username)
        self.chatInterface = ChatInterface(self.client, self, self.username)

        self.navigationInterface.setAcrylicEnabled(True)

        self.initNavigation()
        self.splashScreen.finish()

    def initNavigation(self):
        """初始化导航栏"""
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('主页'))
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.friendInterface, FIF.ROBOT, self.tr('好友'))
        self.addSubInterface(self.chatInterface, FIF.CHAT, self.tr('聊天'))

    def initWindow(self):
        """初始化窗口设置"""
        self.resize(1024, 760)
        self.setResizeEnabled(False)
        self.setMinimumWidth(760)
        self.setWindowIcon(
            QIcon(":/images/logo.png"))
        self.setWindowTitle('Simple-Chat')

        self.setMicaEffectEnabled(True)
        if self.setMicaEffectEnabled(True):
            print(True)

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(100, 100))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def resizeEvent(self, e):
        """重写调整窗口大小事件"""
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())


if __name__ == '__main__':
    """主程序入口"""
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    window = MainWindow()
    window.show()
    app.exec_()
