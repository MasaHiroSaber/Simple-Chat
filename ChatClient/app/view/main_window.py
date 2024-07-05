import sys

from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QApplication

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen)
from qfluentwidgets import FluentIcon as FIF
from ChatClient.app.common.signal_bus import signalBus

from ChatClient.app.view.home_interface import HomeInterface
from ChatClient.app.view.friend_interface import FriendInterface


class MainWindow(FluentWindow):
    def __init__(self, username=None):
        super().__init__()
        self.initWindow()

        self.username = username
        self.homeInterface = HomeInterface(self, self.username)
        self.friendInterface = FriendInterface(self, self.username)

        self.navigationInterface.setAcrylicEnabled(True)
        # self.connectSignalToSlot()

        self.initNavigation()
        self.splashScreen.finish()

    # def connectSignalToSlot(self):
    #     signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
    # signalBus.switchToSampleCard.connect(self.switchToFuntion)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('主页'))
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.friendInterface, FIF.ROBOT, self.tr('好友'))
        # self.addSubInterface()

        # self.addSubInterface()

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(
            QIcon("D:\JetBrains\MasaHiroSaber\PyCharmProjects\Simple-Chat\ChatClient\\app\\resource\images\logo.png"))
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
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    # def switchToFunction(self, routeKey, index):
    #     interfaces = self.findChildren(HomeFunctionInterface)
    #     for w in interfaces:
    #         if w.objectName() == routeKey:
    #             self.stackedWidget.setCurrentWidget(w, False)
    #             w.scrollToCard(index)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    window = MainWindow()
    window.show()
    app.exec_()
