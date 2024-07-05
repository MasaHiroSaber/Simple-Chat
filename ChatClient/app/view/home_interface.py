import asyncio

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap, QPainterPath, QPainter, QLinearGradient, QColor, QBrush, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import ScrollArea, isDarkTheme, AvatarWidget, PillToolButton, StrongBodyLabel
from ChatClient.app.common.style_sheet import StyleSheet
from qfluentwidgets import FluentIcon as FIF
from ChatClient.app.resource import resource_rc


class BannerWidget(QWidget):

    def __init__(self, parent=None, username="Unknown", avatar="def"):
        super().__init__(parent=parent)
        self.setFixedHeight(336)

        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel('主页', self)
        self.banner = QPixmap(':/images/header1.png')
        self.galleryLabel.setObjectName('galleryLabel')
        self.avatarImage = AvatarWidget(self)
        self.avatarImage.setPixmap(QPixmap(':/images/mhs.jpg'))
        self.avatarImage.setFixedSize(96, 96)
        self.avatarImage.move(40, 200)

        self.changeAvatarImage = PillToolButton(self)
        self.changeAvatarImage.setIcon(FIF.EDIT)
        self.changeAvatarImage.setFixedSize(36, 36)
        self.changeAvatarImage.setCheckable(False)
        self.changeAvatarImage.move(105, 265)

        self.welcomeLabel = StrongBodyLabel('你好!', self)
        self.welcomeLabel.setStyleSheet('font-size: 20px')
        self.welcomeLabel.setMinimumWidth(300)
        self.welcomeLabel.move(160, 230)

        self.userNameLabel = StrongBodyLabel(username, self)
        self.userNameLabel.setStyleSheet('font-size: 26px')
        self.userNameLabel.setMinimumWidth(300)
        self.userNameLabel.move(160, 260)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 20, 0, 0)
        self.vBoxLayout.addWidget(self.galleryLabel)
        # self.vBoxLayout.addWidget(self.avatarImage)
        self.vBoxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        w, h = self.width(), self.height()
        path.addRoundedRect(QRectF(0, 0, w, h), 10, 10)
        path.addRect(QRectF(0, h - 50, 50, 50))
        path.addRect(QRectF(w - 50, 0, 50, 50))
        path.addRect(QRectF(w - 50, h - 50, 50, 50))
        path = path.simplified()

        # init linear gradient effect
        gradient = QLinearGradient(0, 0, 0, h)

        # draw background color
        if not isDarkTheme():
            gradient.setColorAt(0, QColor(207, 216, 228, 255))
            gradient.setColorAt(1, QColor(207, 216, 228, 0))
        else:
            gradient.setColorAt(0, QColor(0, 0, 0, 255))
            gradient.setColorAt(1, QColor(0, 0, 0, 0))

        painter.fillPath(path, QBrush(gradient))

        # draw banner image
        pixmap = self.banner.scaled(
            self.size(), transformMode=Qt.SmoothTransformation)
        painter.fillPath(path, QBrush(pixmap))


class HomeInterface(ScrollArea):
    def __init__(self, parent=None, username="Unknown", avatar="def"):
        super().__init__(parent=parent)

        self.banner = BannerWidget(self, username, avatar)
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        # self.loadSamples()

    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')

        StyleSheet.HOME_INTERFACE.apply(self)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
