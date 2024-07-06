from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextBrowser, QWidget
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtCore import Qt
import sys

from ChatClient.app.resource.utils.setQuestion import SetQuestion
from ChatClient.app.resource.utils.Ui import UiCharSession


class ChatSession(QWidget, UiCharSession):
    def __init__(self, parent=None, icon=":/images/mhs.jpg", name="first"):
        super(ChatSession, self).__init__(parent)


        self.setupUi(self)
        self.sum = 0  # 气泡数量
        self.widgetList = []  # 记录气泡
        self.text = ""  # 存储信息
        self.icon = QtGui.QPixmap(icon)  # 头像

        # 设置聊天窗口样式 隐藏滚动条
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 信号与槽
        self.pushButton.clicked.connect(self.createWidget)  # 创建气泡
        self.pushButton.clicked.connect(self.setWidget)  # 修改气泡长宽

        # 监听输入框状态，用于读取是换行还是发送
        self.plainTextEdit.undoAvailable.connect(self.Event)

        # 监听窗口滚动条范围
        scrollbar = self.scrollArea.verticalScrollBar()
        scrollbar.rangeChanged.connect(self.adjustScrollToMaxValue)

        # 是否初始化
        self.ifInit = 0
        self.name = name
    # 回车键绑定发送
    def Event(self):
        """
        重写了keypressevent方法
        同时摁event.modifiers() == Qt.ShiftModifier
        也就shift和回车的时候会换行

        如果只是摁回车键的话，调用
        self.setEnabled(False) ，并触发undoAvailable
        :return:
        """
        if not self.plainTextEdit.isEnabled():  # 如果 plainTextEdit 控件当前不可用（不可输入），执行下面的代码。
            self.plainTextEdit.setEnabled(True)
            self.pushButton.click()  # 触发点击事件
            self.plainTextEdit.setFocus()  # 将输入焦点设置到 plainTextEdit 控件上

    # 创建气泡
    # 这里是左右气泡
    def createWidget(self):
        self.text = self.plainTextEdit.toPlainText()
        self.plainTextEdit.setPlainText("")
        self.sum += 1
        if self.sum % 2:  # 根据判断创建左右气泡
            SetQuestion.setReturn(self, self.icon, self.text, QtCore.Qt.LeftToRight)  # 调用new_widget.py中方法生成左气泡
            QApplication.processEvents()  # 等待并处理主循环事件队列
        else:
            SetQuestion.setReturn(self, self.icon, self.text, QtCore.Qt.RightToLeft)  # 调用new_widget.py中方法生成右气泡
            QApplication.processEvents()  # 等待并处理主循环事件队列

    # 修改气泡
    def setWidget(self):
        font = QFont()
        font.setPointSize(16)
        fm = QFontMetrics(font)
        text_width = fm.width(self.text) + 115  # 根据字体大小生成适合的气泡宽度
        if self.sum != 0:
            if text_width > 632:  # 宽度上限
                text_width = int(self.textBrowser.document().size().width()) + 100  # 固定宽度
            self.widget.setMinimumSize(text_width, int(self.textBrowser.document().size().height()) + 40)  # 规定气泡大小
            self.widget.setMaximumSize(text_width, int(self.textBrowser.document().size().height()) + 40)  # 规定气泡大小
            self.scrollArea.verticalScrollBar().setValue(10)

    # 窗口滚动到最底部
    def adjustScrollToMaxValue(self):
        scrollbar = self.scrollArea.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
