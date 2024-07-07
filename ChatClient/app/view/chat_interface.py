import asyncio
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot, QSize, QRect, pyqtSignal
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QLabel, QBoxLayout, QSizePolicy
from qfluentwidgets import ScrollArea, ListWidget, PushButton, SingleDirectionScrollArea, PlainTextEdit, \
    ToolButton, FluentIcon, AvatarWidget, BodyLabel

from ChatClient.app.common.style_sheet import StyleSheet


class MyMessageBox(QWidget):
    def __init__(self, sender, receive, isUserSend,message='Hello'):
        super().__init__()
        self.sender = sender
        self.receive = receive
        self.message = message
        self.isUserSend = isUserSend

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.avatar = AvatarWidget(self)
        avatar_path = f"../resource/temp/{self.sender}_avatar.jpg"

        if os.path.exists(avatar_path):
            self.avatar.setPixmap(QPixmap(avatar_path))
        else:
            self.avatar.setPixmap(QPixmap(':/images/mhs.jpg'))

        # self.avatar.setPixmap(QPixmap(':/images/mhs.jpg'))
        self.avatar.setRadius(16)
        layout.addWidget(self.avatar)

        self.messageContent = BodyLabel(self)
        self.messageContent.setText(self.message)
        if self.isUserSend:
            self.messageContent.setStyleSheet("""
                QLabel {
                    background-color: rgb(100,210,248);
                    border-radius: 15px;
                    padding: 10px;
                    color: white;
                }
            """)
        else:
            self.messageContent.setStyleSheet("""
                QLabel {
                    background-color: rgb(200,200,200);
                    border-radius: 15px;
                    padding: 10px;
                    color: white;
                }
            """)
            
        layout.addWidget(self.messageContent)

        if self.isUserSend:
            layout.setDirection(QBoxLayout.RightToLeft)
            
        self.setLayout(layout)


class ChatInterface(ScrollArea):
    on_get_message = pyqtSignal(list)
    on_send_message = pyqtSignal()

    def __init__(self, client, parent=None, username=None):
        super().__init__(parent=parent)
        self.client = client
        self.username = username
        self.currentChatFriend = None
        self.friends = None
        self.messageTask = None
        self.difMessage = None
        self.view = QWidget(self)
        self.hBoxLayout = QHBoxLayout(self.view)

        self.parent().friendInterface.on_get_user_friends.connect(self.refreshWidget)
        self.on_get_message.connect(self.getFriendMessage)

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
        self.sendButton.clicked.connect(self.useSendMessage)

        self.chatSession = SingleDirectionScrollArea(orient=Qt.Vertical)
        self.chatSession.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chatSession.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chatSession.setStyleSheet('SingleDirectionScrollArea{border: 1px solid gray;' 'border-radius: 20px;}')

        scrollbar = self.chatSession.verticalScrollBar()
        scrollbar.rangeChanged.connect(self.adjustScrollToMaxValue)

        self.MessageSendingBox = PlainTextEdit()
        # self.MessageSendingBox.setStyleSheet('PlainTextEdit{border: 2px solid gray;' 'border-radius: '
        #                                      '10px;}')
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

    def adjustScrollToMaxValue(self):
        scrollbar = self.chatSession.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def setChatSession(self, currentChatFriend, messageData=None):
        if messageData:
            view = QWidget()
            view.setMinimumWidth(self.chatSession.width())
            layout = QVBoxLayout(view)
            for message in reversed(messageData):
                if message[0] == self.username:
                    layout.addWidget(MyMessageBox(sender=message[0], receive=message[1], message=message[2], isUserSend=True),
                                     alignment=Qt.AlignRight)
                else:
                    layout.addWidget(MyMessageBox(sender=message[0], receive=message[1], message=message[2], isUserSend=False),
                                     alignment=Qt.AlignLeft)
            self.chatSession.setWidget(view)
            # self.chatSession.widgetResizable()
            # pass
 
        self.adjustScrollToMaxValue()


    def initChatSession(self):
        self.currentChatFriend = self.friendList.item(0)
        self.friendList.setCurrentItem(self.currentChatFriend)

    def refreshFriendsListWidget(self):
        stands = []
        for friend in self.friends:
            stands.append(friend[0])

        self.friendList.addItems(stands)

    def refreshChatSession(self):
        self.currentChatFriend = self.friendList.currentItem().text()
        # self.setChatSession(self.currentChatFriend)
        self.stop_chat()
        self.useGetMessage()
        # print(self.currentChatFriend)

    def useGetMessage(self):
        asyncio.run_coroutine_threadsafe(self.GetMessageStart(self.currentChatFriend), self.client.loop)

    async def GetMessageStart(self, friend_username):
        self.messageTask = asyncio.create_task(self.getMessage(friend_username))
        await self.messageTask

    async def getMessage(self, friendName):
        while True:
            message = await self.client.chat_handler.cget_messages(self.username, friendName)
            self.on_get_message.emit(message['response'])
            # await self.client.chat_handler.csend_message(self.username, friendName, messageContent)
            await asyncio.sleep(2)
    
    def useSendMessage(self):
        message = self.MessageSendingBox.toPlainText()
        if message:
            asyncio.run_coroutine_threadsafe(self.sendMessageStart(self.currentChatFriend, messageContent=message), self.client.loop)

    async def sendMessageStart(self, friendName, messageContent=None):
        self.messageTask = asyncio.create_task(self.sendMessage(friendName, messageContent))

    async def sendMessage(self, friendName, messageContent=None):
        await self.client.chat_handler.csend_message(self.username, friendName, messageContent)

    def stop_chat(self):
        if self.messageTask is not None:
            self.messageTask.cancel()  # 取消当前任务
            self.messageTask = None

    @pyqtSlot()
    def refreshWidget(self):
        self.friends = self.parent().userFriends
        self.refreshFriendsListWidget()
        # self.initChatSession()

    @pyqtSlot(list)
    def getFriendMessage(self, message):
        self.setChatSession(self.currentChatFriend, message)
        pass
