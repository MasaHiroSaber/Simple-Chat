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
        self.incoming_avatars = {}

    async def handle_client(self, reader, writer):
        while True:
            await writer.drain()
            data = await reader.read(4096)

            if not data:
                print('script client disconnected')
                writer.close()  # 关闭套接字
                await writer.wait_closed()  # 等待套接字完全关闭
                return

            message = data.decode('utf-8')
            addr = writer.get_extra_info('peername')
            logging.info(f"Received {message} from {addr}")

            response = await self.process_message(message, writer, reader)
            if response:
                writer.write(response.encode('utf-8'))
                await writer.drain()
            logging.info(f"Send: {response}")

    async def process_message(self, message, writer, reader):
        try:
            message_data = json.loads(message)
        except json.JSONDecodeError as e:
            logging.error(e)
            return json.dumps({'success': False, 'response': 'Invalid message format'})
        message_type = message_data.get('type')
        match message_type:
            case 'update_avatar':
                username = message_data['username']
                chunk = message_data['avatar_chunk']
                chunk_index = message_data['chunk_index']
                total_chunks = message_data['total_chunks']

                if username not in self.incoming_avatars:
                    self.incoming_avatars[username] = [''] * total_chunks
                self.incoming_avatars[username][chunk_index] = chunk

                if all(self.incoming_avatars[username]):
                    avatarBase64 = ''.join(self.incoming_avatars[username])
                    success, response = self.user_manager.update_avatar(username, avatarBase64)
                    del self.incoming_avatars[username]
                else:
                    success, response = True, f"Received chunk {chunk_index + 1}/{total_chunks}"

            case 'register':
                success, response = self.user_manager.register_user(
                    message_data['username'], message_data['password'])
            case 'login':
                success, response = self.user_manager.login_user(
                    message_data['username'], message_data['password'])
            case 'get_user_details':
                username = message_data['username']
                user_details = self.user_manager.get_user_details(username)
                if user_details:
                    avatar_data = user_details[1][0][2]
                    chunk_size = 2048
                    total_chunks = (len(avatar_data) + chunk_size - 1) // chunk_size
                    initial_response = json.dumps({'success': True, 'total_chunks': total_chunks})
                    writer.write(initial_response.encode('utf-8'))
                    await writer.drain()

                    for chunk_index in range(total_chunks):
                        await asyncio.sleep(0.01)
                        chunk_start = chunk_index * chunk_size
                        chunk_end = chunk_start + chunk_size
                        chunk = avatar_data[chunk_start:chunk_end]
                        chunk_response = {
                            'success': True,
                            'avatar_chunk': chunk,
                        }
                        logging.info(f"Send: {chunk_response}")
                        writer.write(json.dumps(chunk_response).encode('utf-8'))
                        await writer.drain()
                    return
                else:
                    success, response = False, "User not found"
                # success, response = self.user_manager.get_user_details(
                #     message_data['username'])
            case 'get_user_friends':
                success, response = self.user_manager.get_user_friends(
                    message_data['username'])
            case 'get_all_users':
                success, response = self.user_manager.get_all_users(
                    message_data['username'])
            case 'send_friend_request':
                success, response = self.user_manager.send_friend_request(
                    message_data['sender_username'], message_data['receiver_username'])
            case 'respond_friend_request':
                success, response = self.user_manager.respond_friend_request(
                    message_data['request_id'], message_data['response'])
            case 'get_friend_requests':
                success, response = self.user_manager.get_friend_requests(
                    message_data['username'])
            case 'send_message':
                success, response = self.chat_manager.send_message(
                    message_data['sender_id'], message_data['receiver_id'],
                    message_data['message'], message_data['msg_type'])
            case 'connect':
                success = True
                response = 'connect success'
            case _:
                success, response = False, "Unknown message type"

        return json.dumps({'success': success, 'response': response})

    async def run_server(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        addr = server.sockets[0].getsockname()
        logging.info(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

    def start(self):
        asyncio.run(self.run_server())
        # self.loop.run_until_complete(self.run_server())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    chat_server = ChatServer()
    chat_server.start()
