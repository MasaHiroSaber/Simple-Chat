from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot, QSize, QRect
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QLabel
from qfluentwidgets import ScrollArea, ListWidget, PushButton, SingleDirectionScrollArea, PlainTextEdit, \
    ToolButton, FluentIcon

from ChatClient.app.common.style_sheet import StyleSheet


class MyMessageBox(QWidget):
    def __init__(self, ico, text, direction=Qt.LeftToRight):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()



class ChatInterface(ScrollArea):

    def __init__(self, client, parent=None, username=None):
        super().__init__(parent=parent)
        self.client = client
        self.username = username
        self.currentChatFriend = None
        self.friends = None
        self.messageTask = None
        self.view = QWidget(self)
        self.hBoxLayout = QHBoxLayout(self.view)

        self.parent().friendInterface.on_get_user_friends.connect(self.refreshWidget)

        self.__initWidgets__()

    def __initWidgets__(self):
        # 用于初始生成右侧页面的
        self.view.setObjectName('view')
        self.setObjectName('chatInterface')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.rightLayout.setContentsMargins(10, 0, 10, 0)

        self.rightTopLayout = QVBoxLayout()
        self.rightBottomLayout = QHBoxLayout()
        # 设置左侧widget
        self.friendList = ListWidget()
        self.friendList.setMaximumWidth(200)
        self.friendList.setSelectRightClickedRow(True)
        self.friendList.itemSelectionChanged.connect(self.refreshChatSession)
        self.sendButton = ToolButton()
        self.sendButton.setIcon(FluentIcon.SEND)
        self.sendButton.setIconSize(QSize(30, 30))
        self.sendButton.setFixedSize(80, 80)
        self.sendButton.clicked.connect(self.sendChatMessage)

        self.chatSession = SingleDirectionScrollArea(orient=Qt.Vertical)
        self.chatSession.setStyleSheet('SingleDirectionScrollArea{border: 1px gray;' 'border-radius: 20px;}')
        self.MessageSendingBox = PlainTextEdit()
        # self.MessageSendingBox.setStyleSheet('PlainTextEdit{border: 3px solid gray;' 'border-radius: '
        #                                      '20px;}')
        self.MessageSendingBox.setMinimumHeight(80)
        self.MessageSendingBox.setMaximumHeight(80)

        self.hBoxLayout.addLayout(self.leftLayout)
        self.hBoxLayout.addLayout(self.rightLayout)
        self.leftLayout.addWidget(self.friendList)

        self.rightLayout.addLayout(self.rightTopLayout)
        self.rightLayout.addLayout(self.rightBottomLayout)

        self.rightTopLayout.addWidget(self.chatSession)
        self.rightBottomLayout.addWidget(self.MessageSendingBox)
        self.rightBottomLayout.addWidget(self.sendButton)

        QScrollArea.setStyleSheet(self, 'background-color: transparent')

        self.icon = QtGui.QPixmap(":/images/mhs.jpg")

        StyleSheet.CHAT_INTERFACE.apply(self)

    def setChatSession(self, currentChatFriend):

        view = QWidget()
        layout = QVBoxLayout(view)
        for i in range(1, 50):
            layout.addWidget(MyMessageBox(self, self.icon, 'self.text', Qt.LeftToRight))
        self.chatSession.setWidget(view)
        pass

    def initChatSession(self):
        self.currentChatFriend = self.friendList.item(0)
        self.friendList.setCurrentItem(self.currentChatFriend)
        view = QWidget()
        layout = QVBoxLayout(view)
        for i in range(1, 50):
            layout.addWidget(PushButton(f"按钮 {i}"))
        self.chatSession.setWidget(view)

    def refreshFriendsListWidget(self):
        stands = []
        for friend in self.friends:
            stands.append(friend[0])

        self.friendList.addItems(stands)

    def refreshChatSession(self):
        self.currentChatFriend = self.friendList.currentItem().text()
        self.setChatSession(self.currentChatFriend)
        print(self.currentChatFriend)

    def sendChatMessage(self):
        self.start_chat(self.currentChatFriend)

    async def messageHandler(self, friendName, message=''):
        pass

    def start_chat(self, friend_username, message=''):
        self.currentChatFriend = friend_username
        pass

    def stop_chat(self):
        pass

    @pyqtSlot()
    def refreshWidget(self):
        self.friends = self.parent().userFriends
        self.refreshFriendsListWidget()
        self.initChatSession()
