# -- coding: utf-8 --**
import asyncio
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from qframelesswindow import AcrylicWindow
from qfluentwidgets import setThemeColor, SplitTitleBar, InfoBar
from ChatClient.app.ui.login_window import Ui_Form
from ChatClient.app.common.info_bar import info_bar


class LoginWindow(AcrylicWindow, Ui_Form):
    # 登录成功信号
    login_success = pyqtSignal(str)
    # 显示错误信号
    show_error = pyqtSignal(str, str)
    # 显示成功信号
    show_success = pyqtSignal(str, str)

    def __init__(self, client):
        super().__init__()
        self.setupUi(self)
        self.client = client

        # setTheme(Theme.DARK)
        setThemeColor('#28afe9')

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()
        
        self.remeberpw_checkBox.setEnabled(False)

        self.label.setScaledContents(False)
        self.setWindowTitle('Login')
        self.setWindowIcon(QIcon(":/images/logo.png"))
        self.resize(1000, 650)

        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False)
        self.setStyleSheet("LoginWindow{background: rgba(242, 242, 242, 0.8)}")
        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.bindFuntions()

        self.login_button.setEnabled(False)
        self.register_button.setEnabled(False)

        self.show_error.connect(self.show_error_message)
        self.show_success.connect(self.show_success_message)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap(":/images/background.jpg").scaled(
            self.label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

    def bindFuntions(self):
        # 绑定登录按钮点击事件
        self.login_button.clicked.connect(self.userLogin)
        # 绑定注册按钮点击事件
        self.register_button.clicked.connect(self.userRegister)

    def userLogin(self):
        # 获取用户名和密码
        username = self.username_lineEdit.text()
        password = self.password_lineEdit.text()
        if username and password:
            asyncio.run_coroutine_threadsafe(self.login(username, password), self.client.loop)
        else:
            info_bar(InfoBar.error, self, '错误', '您输入的用户名或密码为空')

    async def login(self, username, password):
        # 异步登录处理
        response = await self.client.user_handler.login(username, password)
        if response['success']:
            self.login_success.emit(str(username))
            self.show_success.emit('成功', '登录成功！')
        else:
            self.show_error.emit('错误', '您输入的用户名或密码有误！')
            pass

    def userRegister(self):
        # 获取用户名和密码
        username = self.username_lineEdit.text()
        password = self.password_lineEdit.text()
        if username and password:
            asyncio.run_coroutine_threadsafe(self.register(username, password), self.client.loop)
        else:
            info_bar(InfoBar.error, self, '错误', '您输入的用户名或密码为空')

    async def register(self, username, password):
        # 异步注册处理
        response = await self.client.user_handler.register(username, password)
        if response['success']:
            self.login_success.emit(str(username))
            self.show_success.emit('成功', '注册成功！')
        else:
            self.show_error.emit('错误', '您输入的用户名已被注册！')
            pass

    def on_connection_established(self):
        # 连接建立后启用登录和注册按钮
        self.login_button.setEnabled(True)
        self.register_button.setEnabled(True)
        info_bar(InfoBar.success, self, 'Bingo', '你已成功连接到服务器')

    @pyqtSlot(str, str)
    def show_error_message(self, title, message):
        # 显示错误信息
        info_bar(InfoBar.error, self, title, message)

    @pyqtSlot(str, str)
    def show_success_message(self, title, message):
        # 显示成功信息
        info_bar(InfoBar.success, self, title, message)
        
    @pyqtSlot(str)
    def get_username_message(self, username):
        # 获取用户名信息
        return username
