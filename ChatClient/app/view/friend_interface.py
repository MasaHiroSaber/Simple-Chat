import asyncio
import base64
import logging
import os
import threading

from PyQt5.QtCore import Qt, QSize, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPainter, QPen, QColor, QIcon, QDesktopServices, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QScrollArea, QFrame, QHBoxLayout, QToolButton, \
    QCompleter, QPushButton
from qfluentwidgets import ScrollArea, SearchLineEdit, isDarkTheme, PushButton, BodyLabel, StrongBodyLabel, IconWidget, \
    FluentIcon, AvatarWidget, InfoBar, ToolButton, InfoBadge, InfoBadgePosition, DotInfoBadge, InfoBarPosition
from ChatClient.app.resource import resource_rc
from ChatClient.app.common.style_sheet import StyleSheet
from ChatClient.app.ui.friend_requests_show import FriendRequestWindow
from ChatClient.app.ui.user_detail_show import UserDetailWindow
from ChatClient.app.common.info_bar import info_bar
from qfluentwidgets import FluentIcon as FIF


class Friend(QWidget):
    """好友卡片类，用于显示好友信息"""
    def __init__(self, widget_username: QWidget, widget_avatar: QWidget, stretch=0, parent=None):
        super().__init__(parent=parent)
        self.parent = parent
        self.widget_username = widget_username
        self.widget_avatar = widget_avatar
        self.stretch = stretch

        self.card = QFrame(self)

        self.sourceWidget = QFrame(self.card)
        self.chatLcon = IconWidget(FluentIcon.CHAT, self.sourceWidget)

        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = QVBoxLayout(self.card)
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout(self.sourceWidget)

        self.__initWidget()

    def __initWidget(self):
        """初始化组件"""
        self.chatLcon.setFixedSize(16, 16)
        self.__initLayout()

        self.sourceWidget.setCursor(Qt.PointingHandCursor)
        self.sourceWidget.installEventFilter(self)

        self.card.setObjectName('card')
        self.sourceWidget.setObjectName('sourceWidget')

    def __initLayout(self):
        """初始化布局"""
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
        self.bottomLayout.addWidget(self.chatLcon, 0, Qt.AlignRight)
        self.bottomLayout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


class FriendInterface(ScrollArea):
    on_send_friend_request = pyqtSignal(bool)
    on_respond_friend_request = pyqtSignal(list)
    on_get_friend_request = pyqtSignal(list)
    on_get_user_friends = pyqtSignal()
    on_get_all_users = pyqtSignal(list)
    on_get_friend_details = pyqtSignal()

    def __init__(self, client, parent=None, username="None"):
        super().__init__(parent=parent)
        self.client = client
        self.username = username
        self.friends = None
        self.users = None
        self.friendRequest = None
        self.friendsDetails = []

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.on_get_user_friends.connect(self.updateFriends)
        self.on_get_all_users.connect(self.updateUsers)
        self.on_get_friend_request.connect(self.getRequests)
        self.on_send_friend_request.connect(self.addFriendSuccess)
        self.on_get_friend_details.connect(self.saveImage)

        self.asyncFunctions()
        self.__initWidgets()

    def useRefreshFriends(self):
        asyncio.run_coroutine_threadsafe(self.refreshFriends(), self.client.loop)

    def useGetUserFriendsDetails(self):
        asyncio.run_coroutine_threadsafe(self.getUserFriendsDetails(), self.client.loop)

    def useGetUserFriends(self):
        asyncio.run_coroutine_threadsafe(self.getUserFriends(self.username), self.client.loop)

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
        self.userSearchEdit.setFixedWidth(200)
        self.userSearchEdit.searchSignal.connect(self.openUserDetailsWindow)

        self.friendRequestButton = ToolButton(self)
        self.friendRequestButton.setIcon(FIF.SEND)
        self.friendRequestButton.clicked.connect(self.openFriendRequestWindow)

        self.refreshButton = ToolButton(self)
        self.refreshButton.setIcon(FIF.SYNC)
        # self.refreshButton.clicked.connect(self.useGetUserFriends)
        self.refreshButton.clicked.connect(self.useRefreshFriends)
        self.refreshButton.clicked.connect(self.refreshFriendsWidget)

        self.topHBoxLayout = QHBoxLayout()
        self.topHBoxLayout.setSpacing(10)
        self.topHBoxLayout.setAlignment(Qt.AlignLeft)

        self.midHBoxLayout = QHBoxLayout()

        self.bottomVBoxLayout = QVBoxLayout()

        self.title = StrongBodyLabel(self)
        self.title.setText('您的好友')
        self.title.setStyleSheet('font-size: 20px')

        self.vBoxLayout.setSpacing(20)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
        self.vBoxLayout.addLayout(self.topHBoxLayout)
        self.vBoxLayout.addLayout(self.midHBoxLayout)
        self.vBoxLayout.addLayout(self.bottomVBoxLayout)
        self.topHBoxLayout.addWidget(self.userSearchEdit, 0, Qt.AlignLeft)
        self.topHBoxLayout.addWidget(self.friendRequestButton, 0, Qt.AlignLeft)
        self.topHBoxLayout.addWidget(self.refreshButton, 0, Qt.AlignLeft)
        self.midHBoxLayout.addWidget(self.title, 0, Qt.AlignLeft)

        StyleSheet.FRIEND_INTERFACE.apply(self)

    def addCurrentFriend(self, widget_username, widget_avatar, stretch=0):
        card = Friend(widget_username, widget_avatar, stretch, self.view)
        self.bottomVBoxLayout.addWidget(card, 0, Qt.AlignTop)
        return card

    # 刷新好友申请徽章
    def refreshBadge(self, num):
        if (num > 0):
            self.infoBadge = DotInfoBadge.success(self, self.friendRequestButton, position=InfoBadgePosition.TOP_RIGHT)
        else:
            self.infoBadge = None

    # 刷新用户
    def refreshUsers(self):
        stand = []
        for user in self.users:
            stand.append(user[1])

        completer = QCompleter(stand, self.userSearchEdit)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setMaxVisibleItems(5)

        self.userSearchEdit.setCompleter(completer)

    # 刷新好友组件
    def refreshFriendsWidget(self):

        item_list = list(range(self.bottomVBoxLayout.count()))
        item_list.reverse()

        for i in item_list:
            item = self.bottomVBoxLayout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        for friend in self.friends:
            avatar_path = f"../resource/temp/{friend[0]}_avatar.jpg"

            if os.path.exists(avatar_path):
                avatarWidget = AvatarWidget(avatar_path)
            else:
                avatarWidget = AvatarWidget(':/images/mhs.jpg')
            # avatarWidget.setPixmap(QPixmap(':/images/mhs.jpg'))
            avatarWidget.setRadius(32)
            userName = StrongBodyLabel()
            userName.setText(str(friend[0]))
            userName.setStyleSheet('font-size: 16px;')
            self.addCurrentFriend(
                userName,
                avatarWidget,
            )

    def checkAvatarImageExist(self, avatar_path):
        if os.path.exists(avatar_path):
            return True
        else:
            return False

    # 储存图像
    @pyqtSlot()
    def saveImage(self):
        data = self.friendsDetails
        for friendDetail in data:
            friendName = friendDetail['username']
            if friendDetail['avatar'] != 'default':
                friendAvatarData = base64.b64decode(friendDetail['avatar'])

                save_dir = '../resource/temp'
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                image_file_name = f'{friendName}_avatar.jpg'
                image_file_path = os.path.join(save_dir, image_file_name)

                with open(image_file_path, 'wb') as image_file:
                    image_file.write(friendAvatarData)

    # 执行异步函数
    async def asyncTask(self):
        # await asyncio.sleep(1) asyncio.create_task(self.parent().homeInterface.getCurrentUserDetails(self.username))
        task1 = asyncio.create_task(self.parent().homeInterface.getCurrentUserDetails(self.username))
        await task1
        task2 = asyncio.create_task(self.getUserFriends(self.username))
        await task2
        task3 = asyncio.create_task(self.getFriendRequests(self.username))
        await task3
        task4 = asyncio.create_task(self.getAllUsers(self.username))
        await task4
        task5 = asyncio.create_task(self.getUserFriendsDetails())
        await task5

    async def refreshFriends(self):
        task1 = asyncio.create_task(self.getUserFriends(self.username))
        await task1
        task2 = asyncio.create_task(self.getUserFriendsDetails())
        await task2

    async def delay(self, time):
        await asyncio.sleep(time)

    async def getAllUsers(self, username):
        response = await self.client.user_handler.get_all_users(username)
        if response['success']:
            self.on_get_all_users.emit(response['response'])
        else:
            pass

    # 获取当前用户好友的详情信息
    async def getUserFriendsDetails(self):
        # self.useGetUserFriends()
        friendName = []
        for friend in self.friends:
            friendName.append(friend[0])
        for name in friendName:
            response = await self.client.user_handler.get_user_details(name)
            if response['success']:
                responseData = response['response']
                self.friendsDetails.append(responseData)
            else:
                pass
        self.on_get_friend_details.emit()
        self.on_get_user_friends.emit()

    # 获取当前用户的好友
    async def getUserFriends(self, username):
        response = await self.client.user_handler.get_user_friends(username)
        if response['success']:
            self.friends = response['response']
        else:
            pass

    # 获取数据库中的好友申请
    async def getFriendRequests(self, username):
        response = await self.client.user_handler.get_friend_requests(username)
        if response['success']:
            self.on_get_friend_request.emit(response['response'])
        else:
            pass

    # 发送好友申请
    async def sendFriendRequest(self, sender_username, receiver_username):
        response = await self.client.user_handler.send_friend_request(sender_username, receiver_username)
        self.on_send_friend_request.emit(response['success'])

    # 回应好友申请
    async def respondFriendRequest(self, request_id, response):
        response = await self.client.user_handler.respond_friend_request(request_id, response)
        if response['success']:
            self.on_respond_friend_request.emit(response['response'])
        else:
            pass

    # 打开用户详情
    def openUserDetailsWindow(self, selectUserName):
        userList = []
        friendList = []
        for user in self.users:
            userList.append(user[1])
        for friend in self.friends:
            friendList.append(friend[0])
        if selectUserName in userList:
            self.userDetails = UserDetailWindow(selectUserName)
            self.userDetails.username_label.setText(selectUserName)
            self.userDetails.function_button.setChecked(True)
            self.userDetails.function_button.setCheckable(False)

            avatar_path = f"../resource/temp/{selectUserName}_avatar.jpg"

            if os.path.exists(avatar_path):
                self.userDetails.avatar_image.setPixmap(QPixmap(avatar_path))
            else:
                self.userDetails.avatar_image.setPixmap(QPixmap(':/images/mhs.jpg'))
            self.userDetails.avatar_image.setFixedSize(96, 96)
            if selectUserName in friendList:
                self.userDetails.function_button.setText('发送消息')
                self.userDetails.sendMessage = True
            else:
                self.userDetails.function_button.setText('添加好友')
                self.userDetails.addFriend = True
            self.userDetails.show()

            self.userDetails.on_add_friend.connect(self.onSendFriendRequest)
        else:
            info_bar(InfoBar.error, self, '错误', '该用户不存在')

    # 打开好友申请列表
    def openFriendRequestWindow(self):
        friendRequestWindow = FriendRequestWindow(self.friendRequest)
        friendRequestWindow.show()

        friendRequestWindow.on_reject_request.connect(self.respondRequest)
        friendRequestWindow.on_accept_request.connect(self.respondRequest)
        friendRequestWindow.on_window_close.connect(self.friendRequestsWindowClose)

    @pyqtSlot(list)
    def updateUsers(self, users):
        self.users = users
        self.refreshUsers()

    @pyqtSlot()
    def updateFriends(self):
        self.parent().userFriends = self.friends
        self.refreshFriendsWidget()

    @pyqtSlot(list)
    def getRequests(self, request):
        self.friendRequest = request
        self.refreshBadge(len(self.friendRequest))

    @pyqtSlot(str, str)
    def respondRequest(self, request_id, response):
        asyncio.run_coroutine_threadsafe(self.respondFriendRequest(request_id, response), self.client.loop)

    @pyqtSlot(str)
    def onSendFriendRequest(self, receiver_username):
        sender_username = self.username
        asyncio.run_coroutine_threadsafe(self.sendFriendRequest(sender_username, receiver_username), self.client.loop)

    @pyqtSlot(bool)
    def addFriendSuccess(self, isSuccess):
        if isSuccess:
            info_bar(InfoBar.success, self.userDetails, '成功', '好友申请已发送', position=InfoBarPosition.TOP)
        else:
            info_bar(InfoBar.warning, self.userDetails, '警告', '你已经发送过好友请求了', position=InfoBarPosition.TOP)

    @pyqtSlot()
    def friendRequestsWindowClose(self):
        self.useRefreshFriends()
