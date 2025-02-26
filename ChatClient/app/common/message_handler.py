import asyncio
import json


class MessageHandler:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def csend_message(self, sender_id, receiver_id, message, msg_type='text'):
        request = {
            'type': 'send_message',
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'message': message,
            'msg_type': msg_type
        }
        await self.send_request(request)
        response = await self.receive_response()
        return response

    async def cget_messages(self, user_name, friend_name):
        request = {
            'type': 'get_messages',
            'user_name': user_name,
            'friend_name': friend_name
        }
        await self.send_request(request)
        response = await self.receive_response()
        return response
        # while True:
        #     data = await self.reader.read(100)
        #     if data:
        #         message = json.loads(data.decode())
        #         # Handle the message (e.g., print it, update UI, etc.)
        #         print(f"Received message: {message}")

    async def send_request(self, request):
        self.writer.write(json.dumps(request).encode())
        print('send a request: {}'.format(json.dumps(request).encode('utf-8')))
        await self.writer.drain()

    async def receive_response(self):
        data = await self.reader.read(4096)
        print('received a response: {}'.format(data))
        response = json.loads(data.decode())
        return response
