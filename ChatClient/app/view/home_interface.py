from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import ScrollArea
from ChatClient.app.common.style_sheet import StyleSheet


class HomeInterface(ScrollArea):
    def __init__(self, parent = None):
        super().__init__(parent=parent)
        
        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()
        # self.loadSamples()
        
    def __initWidget(self):
        self.view.setObjectName('view')
        self.setObjectName('homeInterface')
        
        StyleSheet.HOME_INTERFACE.apply(self)
    
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
    
        self.vBoxLayout.setContentsMargins(0, 0, 0, 36)
        self.vBoxLayout.setSpacing(40)
        # self.vBoxLayout.addWidget(self.banner)
        self.vBoxLayout.setAlignment(Qt.AlignTop)