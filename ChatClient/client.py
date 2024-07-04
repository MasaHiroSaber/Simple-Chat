import asyncio
import sys

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMessageBox
from qfluentwidgets import InfoBar

from ChatClient.app.common.user_handler import UserHandler
from ChatClient.app.view.main_window import MainWindow
from app.ui.login_ui import LoginWindow
from ChatClient.app.common.info_bar import info_bar


def handleSignal(message):
    print(message)


class ChatClient(QObject):
    connection_established = pyqtSignal(str)

    def __init__(self, host='127.0.0.1', port=8888):
        super().__init__()
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None
        self.user_handler = None
        self.loop = asyncio.get_event_loop()

    async def connect(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            self.user_handler = UserHandler(self.reader, self.writer)
            self.connection_established.emit('Connection established')
            data = await self.user_handler.connectTest()

        except Exception as e:
            print(f"Failed to connect: {e}")
            QMessageBox.critical(None, "Connection Error", f"Failed to connect to the server: {e}")

    def run(self):
        asyncio.run_coroutine_threadsafe(self.connect(), self.loop)


class ClientThread(QThread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        self.client.loop.run_forever()


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    client = ChatClient()

    client_thread = ClientThread(client)
    client_thread.start()
    # client.connection_established.connect(handleSignal)

    login_window = LoginWindow(client)
    login_window.show()

    client.connection_established.connect(login_window.on_connection_established)

    client.run()


    def onLoginSuccess():
        main_window = MainWindow(client)
        main_window.show()
        login_window.close()


    login_window.login_success.connect(onLoginSuccess)

    app.exec_()

