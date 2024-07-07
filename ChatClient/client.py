import asyncio
import os
import sys
import threading
import shutil

from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication

from ChatClient.app.common.message_handler import MessageHandler
from ChatClient.app.common.user_handler import UserHandler
from ChatClient.app.view.main_window import MainWindow
from app.ui.login_window_show import LoginWindow


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
        self.chat_handler = None
        self.loop = asyncio.get_event_loop()

    async def connect(self):
        try:
            print(f"当前线程:{threading.current_thread()}")
            self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
            self.user_handler = UserHandler(self.reader, self.writer)
            self.chat_handler = MessageHandler(self.reader, self.writer)
            self.connection_established.emit('Connection established')
            data = await self.user_handler.connect_test()

        except Exception as e:
            print(f"Failed to connect: {e}")

    def run(self):
        asyncio.run_coroutine_threadsafe(self.connect(), self.loop)


class ClientThread(QThread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        self.client.loop.run_forever()


if __name__ == '__main__':
    temp_path = '../resource/temp'

    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    else:
        pass
        # shutil.rmtree(temp_path)
        # os.mkdir(temp_path)

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


    def onLoginSuccess(username):
        main_window = MainWindow(client, username)
        main_window.show()

        main_window.setMicaEffectEnabled(True)

        login_window.close()


    login_window.login_success.connect(onLoginSuccess)

    app.exec_()
