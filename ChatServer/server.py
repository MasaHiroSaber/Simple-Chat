import asyncio
import json
import logging

from user_manager import UserManager
from chat_manager import ChatManager


class ChatServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.loop = asyncio.get_event_loop()
        self.user_manager = UserManager()
        self.chat_manager = ChatManager()

    async def handle_client(self, reader, writer):
        while True:
            await writer.drain()
            data = await reader.read(1024)
            
            if not data:
                print('script client disconnected')
                writer.close() # 关闭套接字
                await writer.wait_closed() # 等待套接字完全关闭
                return
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.info(f"data: {data}")
            message = data.decode('utf-8')
            addr = writer.get_extra_info('peername')
    
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.info(f"Received {message} from {addr}")
    
            response = self.process_message(message)
            writer.write(response.encode('utf-8'))
            await writer.drain()
    
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            logging.info(f"Send: {response}")
        


    def process_message(self, message):
        # Here you will process the message
        # This is just an example
        message_data = json.loads(message)
        if message_data['type'] == 'register':
            print('register')
            success, response = self.user_manager.register_user(
                message_data['username'], message_data['password'])
        elif message_data['type'] == 'login':
            success, response = self.user_manager.login_user(
                message_data['username'], message_data['password'])
        elif message_data['type'] == 'update_avatar':
            success, response = self.user_manager.update_avatar(
                message_data['username'], message_data['avatar_path'])
        elif message_data['type'] == 'send_message':
            success, response = self.chat_manager.send_message(
                message_data['sender_id'], message_data['receiver_id'],
                message_data['message'], message_data['msg_type'])
        elif message_data['type'] == 'connect':
            success = True
            response = 'connect success'
        else:
            success, response = False, "Unknown message type"

        return json.dumps({'success': success, 'response': response})

    async def run_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

    def start(self):
        asyncio.run(self.run_server())
        # self.loop.run_until_complete(self.run_server())


if __name__ == '__main__':
    chat_server = ChatServer()
    chat_server.start()
