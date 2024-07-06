from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout
from qfluentwidgets import PushButton


from ChatClient.app.resource.utils.RewitePlainTextEdit import RewritePlainTextEdit


class UiCharSession(object):
    def setupUi(self, ChatSession):
        ChatSession.setObjectName("ChatSession")


        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self)

        # 设置窗口的大小
        self.setFixedWidth(770)

        # frame 和 它内部布局
        self.frame = QtWidgets.QFrame(self)
        self.setStyleSheet("background-color: rgb(246,246,246);"
                           "\nborder-radius:20px;"
                           "\nborder:3px solid #34495e;\n")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # 滚动区域
        self.scrollArea = QtWidgets.QScrollArea(self.frame)
        self.scrollArea.setStyleSheet("border:initial;\nborder: 0px solid;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 758, 398))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)

        # 添加frame到主布局
        self.verticalLayout_3.addWidget(self.frame)

        # 水平布局和文本框
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plainTextEdit = RewritePlainTextEdit(self.frame)
        self.plainTextEdit.setStyleSheet(
            "QPlainTextEdit{\nborder-radius:20px;"
            "\nborder:3px solid #2c3e50;"
            "\nbackground-color: transparent;"
            "\nfont: 12pt \"微软雅黑\";\npadding:5px;\n}")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout.addWidget(self.plainTextEdit)

        # 按钮
        self.pushButton = PushButton(self)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.horizontalLayout.setStretch(0, 5)
        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_3.setStretch(0, 5)
        self.verticalLayout_3.setStretch(1, 1)

        _translate = QtCore.QCoreApplication.translate
        self.pushButton.setText(_translate("ChatSession", "发送"))
