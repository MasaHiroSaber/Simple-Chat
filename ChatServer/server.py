import asyncio
import json
from user_manager import UserManager
from chat_manager import ChatManager

class ChatServer:
    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port
        self.user_manager = UserManager()
        self.chat_manager = ChatManager()

    async def handle_client(self, reader, writer):
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')

        print(f"Received {message} from {addr}")

        response = self.process_message(message)
        writer.write(response.encode())
        await writer.drain()

        print(f"Send: {response}")
        writer.close()

    def process_message(self, message):
        # Here you will process the message
        # This is just an example
        message_data = json.loads(message)
        if message_data['type'] == 'register':
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
        else:
            success, response = False, "Unknown message type"

        return json.dumps({'success': success, 'response': response})

    async def main(self):
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    chat_server = ChatServer()
    asyncio.run(chat_server.main())
