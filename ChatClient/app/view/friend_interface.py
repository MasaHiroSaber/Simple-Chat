import asyncio
import logging
import threading

from PyQt5.QtCore import Qt, QSize, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPainter, QPen, QColor, QIcon, QDesktopServices
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QScrollArea, QFrame, QHBoxLayout, QToolButton, QCompleter
from qfluentwidgets import ScrollArea, SearchLineEdit, isDarkTheme, PushButton, BodyLabel, StrongBodyLabel, IconWidget, \
    FluentIcon, AvatarWidget, InfoBar
from ChatClient.app.resource import resource_rc
from ChatClient.app.common.style_sheet import StyleSheet
from ChatClient.app.ui.user_detail_show import UserDetailWindow
from ChatClient.app.common.info_bar import info_bar


class Friend(QWidget):
    def __init__(self, widget_username: QWidget, widget_avatar: QWidget, stretch=0, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.widget_username = widget_username
        self.widget_avatar = widget_avatar
        self.stretch = stretch

        self.card = QFrame(self)

        self.sourceWidget = QFrame(self.card)
        self.linkIcon = IconWidget(FluentIcon.LINK, self.sourceWidget)

        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = QVBoxLayout(self.card)
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout(self.sourceWidget)

        self.__initWidget()

    def __initWidget(self):
        self.linkIcon.setFixedSize(16, 16)
        self.__initLayout()

        self.sourceWidget.setCursor(Qt.PointingHandCursor)
        self.sourceWidget.installEventFilter(self)

        self.card.setObjectName('card')
        self.sourceWidget.setObjectName('sourceWidget')

    def __initLayout(self):
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.cardLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        self.topLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.setContentsMargins(12, 12, 12, 12)
        self.bottomLayout.setContentsMargins(18, 18, 18, 18)
        self.cardLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.card, 0, Qt.AlignTop)
        self.vBoxLayout.setAlignment(Qt.AlignTop)

        self.cardLayout.setSpacing(0)
        self.cardLayout.setAlignment(Qt.AlignTop)
        self.cardLayout.addLayout(self.topLayout, 0)
        self.cardLayout.addWidget(self.sourceWidget, 0, Qt.AlignBottom)

        self.widget_avatar.setParent(self.card)
        self.topLayout.addWidget(self.widget_avatar)
        if self.stretch == 0:
            self.topLayout.addStretch(1)

        self.widget_avatar.show()

        self.bottomLayout.addWidget(self.widget_username, 0, Qt.AlignTop)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.linkIcon, 0, Qt.AlignRight)
        self.bottomLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class FriendInterface(ScrollArea):
    on_get_user_friends = pyqtSignal(list)
    on_get_all_users = pyqtSignal(list)

    def __init__(self, client, parent=None, username="None"):
        super().__init__(parent=parent)
        self.client = client
        self.username = username
        self.friends = None
        self.users = None

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.on_get_user_friends.connect(self.updateFriends)
        self.on_get_all_users.connect(self.updateUsers)
        

        self.asyncFunctions()
        self.__initWidgets()

    def asyncFunctions(self):
        asyncio.run_coroutine_threadsafe(self.asyncTask(), self.client.loop)

    def __initWidgets(self):
        QScrollArea.setStyleSheet(self, 'background-color: transparent')

        self.view.setObjectName('view')
        self.setObjectName('friendInterface')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.userSearchEdit = SearchLineEdit(self)
        self.userSearchEdit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.userSearchEdit.setPlaceholderText("查询用户")
        self.userSearchEdit.searchSignal.connect(self.openUserDetails)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
        self.vBoxLayout.addWidget(self.userSearchEdit)

        StyleSheet.FRIEND_INTERFACE.apply(self)

    def addCurrentFriend(self, widget_username, widget_avatar, stretch=0):
        card = Friend(widget_username, widget_avatar, stretch, self.view)
        self.vBoxLayout.addWidget(card, 0, Qt.AlignTop)
        return card

    def resizeEvent(self, e):
        super().resizeEvent(e)

    def refreshUsers(self):
        stand = []
        for user in self.users:
            stand.append(user[1])

        completer = QCompleter(stand, self.userSearchEdit)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setMaxVisibleItems(5)

        self.userSearchEdit.setCompleter(completer)

    def refreshFriendsWidget(self):
        for friend in self.friends:
            avatarWidget = AvatarWidget()
            avatarWidget.setFixedSize(50, 50)
            self.addCurrentFriend(
                StrongBodyLabel(friend[0]),
                avatarWidget,
            )

    async def asyncTask(self):
        task1 = asyncio.create_task(self.getAllUsers(self.username))
        await task1
        task2 = asyncio.create_task(self.getUserFriends(self.username))
        await task2

    async def getAllUsers(self, username):
        response = await self.client.user_handler.get_all_users(username)
        if response['success']:
            self.on_get_all_users.emit(response['response'])
        else:
            pass

    async def getUserFriends(self, username):
        response = await self.client.user_handler.get_user_friends(username)
        if response['success']:
            self.on_get_user_friends.emit(response['response'])
        else:
            pass

    def openUserDetails(self, username):
        stand = []
        for user in self.users:
            stand.append(user[1])
        if username in stand:
            pass
            userDetails = UserDetailWindow()
            userDetails.show()
        else:
            info_bar(InfoBar.error, self, '错误', '该用户不存在')

    @pyqtSlot(list)
    def updateFriends(self, friends):
        self.friends = friends
        self.refreshFriendsWidget()

    @pyqtSlot(list)
    def updateUsers(self, users):
        self.users = users
        self.refreshUsers()
