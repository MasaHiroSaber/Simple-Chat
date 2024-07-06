from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QTextBrowser


class SetQuestion:
    def setReturn(self, ico, text, direction):
        """
        :param ico: 头像
        :param text: 文本
        :param direction:方向
        """

        self.widget = QWidget(self.scrollAreaWidgetContents)
        self.widget.setLayoutDirection(direction)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setMaximumSize(QSize(50, 50))
        self.label.setText("")
        self.label.setPixmap(ico)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.textBrowser = QTextBrowser(self.widget)
        self.textBrowser.setLayoutDirection(Qt.LeftToRight)
        self.textBrowser.setStyleSheet("padding:10px;\n"
                                       "background-color: rgba(71,121,214,20);\n"
                                       "font: 16pt \"黑体\";")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setText(text)
        self.textBrowser.setMinimumSize(QSize(0, 0))

        self.textBrowser.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.widget)

