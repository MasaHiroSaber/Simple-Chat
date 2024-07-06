from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import Qt


class RewritePlainTextEdit(QPlainTextEdit):
    # 父类为QplainTextEdit
    def __int__(self, parent=None):
        super(RewritePlainTextEdit, self).__init__(parent)

    def keyPressEvent(self, event: QKeyEvent):
        """"
        重写keypressEvent方法
        同时摁event.modifiers() == Qt.ShiftModifier
        也就shift和回车的时候会换行

        如果只是摁回车键的话，调用
        self.setEnabled(False) ，并触发undoAvailable
        """
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ShiftModifier:      #ctrl+回车
            self.insertPlainText('\n')                                                  #添加换行
        elif self.toPlainText() and event.key() == Qt.Key_Return:                       #回车
            self.sendingFunction()                                                      #调用sendingFunction函数
        else:
            super().keyPressEvent(event)

    def sendingFunction(self):
        self.setEnabled(False)                                                          #主函数使用undoAvailable监听信号
        self.setUndoRedoEnabled(False)                                                  #设置焦点
        self.setUndoRedoEnabled(True)                                                   #设置焦点