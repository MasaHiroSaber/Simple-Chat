from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QScrollArea, QHBoxLayout, QListWidgetItem, QLabel, \
    QPushButton
from qfluentwidgets import ScrollArea, SearchLineEdit, ListWidget

from ChatClient.app.common.style_sheet import StyleSheet
from ChatClient.app.resource.utils.ChatSession import ChatSession


class ChatInterface(ScrollArea):

    def __init__(self, parent=None, username=None, avatar="def"):
        super().__init__(parent=parent)
        self.username = username
        self.avatar = avatar
        self.view = QWidget(self)
        self.hBoxLayout = QHBoxLayout(self.view)

        self.__initWidgets__()

    def __initWidgets__(self):
        # 用于初始生成右侧页面的
        self.judge = 1
        self.p = 0
        self.view.setObjectName('view')
        self.setObjectName('chatInterface')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        StyleSheet.HOME_INTERFACE.apply(self)
        QScrollArea.setStyleSheet(self, 'background-color: transparent')

        # 设置左侧widget
        self.leftWidget = ListWidget()
        self.leftLayout = QVBoxLayout()
        self.leftWidget.setLayout(self.leftLayout)
        self.hBoxLayout.addWidget(self.leftWidget)

        # 用来更新左侧列表，并返回一个含有右侧会话的字典
        # 同时以第一个为右侧最开始的页面
        self.ChatSessionDict, self.stands = self.updateLeftList()

        self.leftWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 通过函数跟新右侧窗口,创建一个临时的Widget
        self.updateRightWidget(list(self.ChatSessionDict.keys())[0])
        self.judge = 0

    def updateRightWidget(self, ChatSName):
        """

        :param
        ChatSName: 传入的是对应的用户名
        :return:
        """

        if not self.judge == 1:
            # 更新字典里面对应的ChatSession
            self.ChatSessionDict[self.p] = self.rightWidget
            # 溢出目前的Widget用来更新
            self.hBoxLayout.removeWidget(self.rightWidget)

        ChatS = self.ChatSessionDict[ChatSName]

        self.rightWidget = ChatSession()
        # 判断该会话有没有过这个流程
        if self.rightWidget.ifInit == 0:
            self.rightLayout = QVBoxLayout()
            self.rightWidget.setLayout(self.rightLayout)

            self.rightWidget.ifInit = 1

        self.p = ChatSName
        self.hBoxLayout.addWidget(self.rightWidget)
        print(self.rightWidget.name + "endif")

    def updateLeftList(self):
        """
        用来跟新左侧用户栏页面的
        stands是储存用户民的列表

        :return:
        """

        # 用来存贮用户民的列表
        stands = [
            'Faker', 'otto', 'monikaBeiZi'
        ]

        # 添加列表项
        for stand in stands:
            item = QListWidgetItem(stand)
            self.leftWidget.addItem(item)

        self.leftWidget.itemClicked.connect(self.displayChat)

        # 创建一个字典储存每一个对象的会话
        rightWidget = {}
        for i in stands:
            self.rightWidget = ChatSession(name=i)
            self.rightLayout = QVBoxLayout()
            self.rightWidget.setLayout(self.rightLayout)
            rightWidget[i] = self.rightWidget

        return rightWidget, stands

    def displayChat(self, item):
        print(f"click :{item.text()}")
        self.updateRightWidget(str(item.text()))
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QScrollArea, QHBoxLayout, QListWidgetItem, QLabel, \
    QPushButton
from qfluentwidgets import ScrollArea, SearchLineEdit, ListWidget

from ChatClient.app.common.style_sheet import StyleSheet
from ChatClient.app.resource.utils.ChatSession import ChatSession


class ChatInterface(ScrollArea):

    def __init__(self, parent=None, username=None, avatar="def"):
        super().__init__(parent=parent)
        self.username = username
        self.avatar = avatar
        self.view = QWidget(self)
        self.hBoxLayout = QHBoxLayout(self.view)

        self.__initWidgets__()





    def __initWidgets__(self):
        # 用于初始生成右侧页面的
        self.judge = 1
        self.p = 0
        self.view.setObjectName('view')
        self.setObjectName('chatInterface')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        StyleSheet.HOME_INTERFACE.apply(self)
        QScrollArea.setStyleSheet(self, 'background-color: transparent')

        # 设置左侧widget
        self.leftWidget = ListWidget()
        self.leftLayout = QVBoxLayout()
        self.leftWidget.setLayout(self.leftLayout)
        self.hBoxLayout.addWidget(self.leftWidget)

        # 用来更新左侧列表，并返回一个含有右侧会话的字典
        # 同时以第一个为右侧最开始的页面
        self.ChatSessionDict, self.stands = self.updateLeftList()


        self.leftWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 通过函数跟新右侧窗口,创建一个临时的Widget
        self.updateRightWidget(list(self.ChatSessionDict.keys())[0])
        self.judge = 0

    def updateRightWidget(self, ChatSName):
        """

        :param
        ChatSName: 传入的是对应的用户名
        :return:
        """

        if not self.judge == 1:

            # 更新字典里面对应的ChatSession
            self.ChatSessionDict[self.p] = self.rightWidget
            # 溢出目前的Widget用来更新
            self.hBoxLayout.removeWidget(self.rightWidget)

        ChatS = self.ChatSessionDict[ChatSName]

        self.rightWidget = ChatSession()
        # 判断该会话有没有过这个流程
        if self.rightWidget.ifInit == 0:

            self.rightLayout = QVBoxLayout()
            self.rightWidget.setLayout(self.rightLayout)

            self.rightWidget.ifInit = 1

        self.p = ChatSName
        self.hBoxLayout.addWidget(self.rightWidget)
        print(self.rightWidget.name+"endif")

    def updateLeftList(self):
        """
        用来跟新左侧用户栏页面的
        stands是储存用户民的列表

        :return:
        """

        # 用来存贮用户民的列表
        stands = [
            'Faker', 'otto', 'monikaBeiZi'
        ]

        # 添加列表项
        for stand in stands:
            item = QListWidgetItem(stand)
            self.leftWidget.addItem(item)

        self.leftWidget.itemClicked.connect(self.displayChat)

        # 创建一个字典储存每一个对象的会话
        rightWidget = {}
        for i in stands:
            self.rightWidget = ChatSession(name=i)
            self.rightLayout = QVBoxLayout()
            self.rightWidget.setLayout(self.rightLayout)
            rightWidget[i] = self.rightWidget

        return rightWidget, stands

    def displayChat(self, item):
        print(f"click :{item.text()}")
        self.updateRightWidget(str(item.text()))
