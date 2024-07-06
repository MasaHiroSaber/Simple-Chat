import asyncio
import base64
import io
import os
import tkinter as tk

from PIL import Image
from tkinter import filedialog

from PyQt5.QtCore import Qt, QRectF, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QPainterPath, QPainter, QLinearGradient, QColor, QBrush, QFont, QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from qfluentwidgets import ScrollArea, isDarkTheme, AvatarWidget, PillToolButton, StrongBodyLabel, InfoBar
from ChatClient.app.common.style_sheet import StyleSheet
from qfluentwidgets import FluentIcon as FIF
from ChatClient.app.common.info_bar import info_bar
from ChatClient.app.resource import resource_rc


class BannerWidget(QWidget):

    def __init__(self, parent=None, username='default', avatar=None):
        super().__init__(parent=parent)
        self.avatarImageData = avatar
        self.setFixedHeight(336)
        self.vBoxLayout = QVBoxLayout(self)
        self.galleryLabel = QLabel('主页', self)
        self.banner = QPixmap(':/images/header1.png')
        self.galleryLabel.setObjectName('galleryLabel')
        self.avatarImage = AvatarWidget(self)
        # self.avatarImage.setFixedSize(96, 96)
        # self.avatarImage.move(40, 200)

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

    # def setAvatarImage(self):
    #     if self.avatarImageData == 'default':
    #         print('isDefault')
    #         self.avatarImage.setPixmap(QPixmap(':/images/mhs.jpg'))
    #     else:
    #         pass
    #         # self.avatarImage.setPixmap(QPixmap(self.avatarImage))

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
    on_update_avatar_success = pyqtSignal(str)

    def __init__(self, client, parent=None, username="Unknown"):
        super().__init__(parent=parent)
        self.client = client
        self.username = username
        self.avatar = 'default'
        self.userDetails = None

        self.banner = BannerWidget(self, self.username, self.avatar)
        self.banner.changeAvatarImage.clicked.connect(self.openChangeAvatarImageSelect)

        self.on_update_avatar_success.connect(self.informationBar)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.__initWidget()
        # self.loadSamples()

        # self.useGetCurrentUserDetails()

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


    # 刷新头像
    def setAvatarImage(self):
        if self.userDetails['avatar'] == 'default':
            self.banner.avatarImage.setPixmap(QPixmap(':/images/mhs.jpg'))
        else:
            # 解码并显示用户头像
            avatarData = base64.b64decode(self.userDetails['avatar'])

            avatarImage = QImage()
            avatarImage.loadFromData(avatarData)

            pixmap = QPixmap.fromImage(avatarImage)

            self.banner.avatarImage.setPixmap(QPixmap(pixmap))

        self.banner.avatarImage.setFixedSize(96, 96)
        self.banner.avatarImage.move(40, 200)

    def useGetCurrentUserDetails(self):
        asyncio.run_coroutine_threadsafe(self.run_tasks_sequentially(), self.client.loop)

    def useChangeAvatarImage(self, avatarImageData):
        asyncio.run_coroutine_threadsafe(self.changeAvatarImage(self.username, avatarImageData), self.client.loop)

    # 打开更改头像选择文件框
    def openChangeAvatarImageSelect(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()

        if file_path:
            with open(file_path, 'rb') as f:
                avatarImageData = f.read()

            avatarImageData = self.compress_and_resize_image(avatarImageData)
            avatarImageData = base64.b64encode(avatarImageData)
            avatarImageData = avatarImageData.decode('utf-8')

            self.useChangeAvatarImage(avatarImageData)

    # 压缩图片
    def compress_and_resize_image(self, image_data, max_size=1024 * 1024):
        # 使用 PIL 打开图像
        image = Image.open(io.BytesIO(image_data))
        image = image.convert('RGB')

        scaling_factor = 256 / max(image.height, image.width)

        # 调整图像大小
        image = image.resize((int(scaling_factor * image.width), int(scaling_factor * image.height)))

        # 将调整大小后的图像保存为二进制数据
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG', quality=50)  # 使用 JPEG 格式保存图像
        img_byte_arr = img_byte_arr.getvalue()

        # 如果图像大小超过指定的最大大小，进行压缩
        while len(img_byte_arr) > max_size:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=25)  # 调整压缩质量
            img_byte_arr = img_byte_arr.getvalue()

        return img_byte_arr

    # 运行异步函数
    async def run_tasks_sequentially(self):
        await self.getCurrentUserDetails(self.username)

    async def getCurrentUserDetails(self, username):
        response = await self.client.user_handler.get_user_details(username)
        if response['success']:
            self.userDetails = response['response']
            print(f"USERDETAILS_RESPONSE: {response}")
            self.setAvatarImage()
        else:
            pass

    async def changeAvatarImage(self, username, avatarImageData):
        response = await self.client.user_handler.update_avatar(username, avatarImageData)
        if response:
            self.on_update_avatar_success.emit('success')
        else:
            pass

    @pyqtSlot(str)
    def informationBar(self, result):
        if result == 'success':
            info_bar(InfoBar.success, self, '成功', '更换头像成功')
            self.useGetCurrentUserDetails()
