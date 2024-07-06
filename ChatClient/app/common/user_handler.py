# -- coding: utf-8 --**
import asyncio
import base64
import json


class UserHandler:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.incoming_details = {}

    async def connect_test(self):
        request = {
            'type': 'connect'
        }
        await self.send_request(request)
        response = await self.receive_response()
        return response

    async def register(self, username, password, avatar='default'):
        request = {
            'type': 'register',
            'username': username,
            'password': password,
            'avatar': avatar
        }
        await self.send_request(request)
        response = await self.receive_response()
        return response

    async def login(self, username, password):
        request = {
            'type': 'login',
            'username': username,
            'password': password
        }
        await self.send_request(request)
        response = await self.receive_response()
        return response

    async def get_user_details(self, username):
        request = {
            'type': 'get_user_details',
            'username': username
        }
        await self.send_request(request)
        initial_response = await self.receive_response()

        if initial_response['success']:
            total_chunks = initial_response['total_chunks']
            task = asyncio.create_task(self.receive_user_details_chunks(username, total_chunks))
            success, avatar_data = await task
            # success, avatar_data = asyncio.ensure_future(self.receive_user_details_chunks(username, total_chunks))
            if success:
                return {'success': True, 'response': {'username': username, 'avatar': avatar_data}}
            else:
                return {'success': False, 'response': 'NONE'}
        else:
            return initial_response
        # response = await self.receive_response()
        # return response

    async def receive_user_details_chunks(self, username, total_chunks):
        avatar_chunks = [''] * total_chunks
        for chunk_index in range(total_chunks):
            response = await self.receive_response()
            if response['success']:
                chunk = response['avatar_chunk']
                avatar_chunks[chunk_index] = chunk
            else:
                print("Error receiving chunk", chunk_index)
                return

        avatar_data = ''.join(avatar_chunks)
        # with open(f"{username}_avatar.png", 'wb') as avatar_file:
        #     avatar_file.write(avatar_data)
        return True, avatar_data

    async def update_avatar(self, username, avatarBase64):
        chunkSize = 2048
        totalChunks = (len(avatarBase64) + chunkSize - 1) // chunkSize

        for i in range(totalChunks):
            chunk = avatarBase64[i * chunkSize:(i + 1) * chunkSize]
            request = {
                'type': 'update_avatar',
                'username': username,
                'avatar_chunk': chunk,
                'chunk_index': i,
                'total_chunks': totalChunks
            }
            await self.send_request(request)
            # await asyncio.sleep(1)
            response = await self.receive_response()
            # return response
        return True

    async def get_all_users(self, username):
        request = {
            'type': 'get_all_users',
            'username': username
        }
        await self.send_request(request)
        response = await self.receive_response()
        return response

    async def get_user_friends(self, username):
        request = {
            'type': 'get_user_friends',
            'username': username
        }
        await self.send_request(request)
        response = await self.receive_response()
        return response

    async def send_friend_request(self, sender_username, receiver_username):
        request = {
            'type': 'send_friend_request',
            'sender_username': sender_username,
            'receiver_username': receiver_username
        }
        await self.send_request(request)
        response = await self.receive_response()
        return response

    async def respond_friend_request(self, request_id, response):
        request = {
            'type': 'respond_friend_request',
            'request_id': request_id,
            'response': response
        }
        await self.send_request(request)
        response = await self.receive_response()
        return response

    async def get_friend_requests(self, username):
        request = {
            'type': 'get_friend_requests',
            'username': username
        }
        await self.send_request(request)
        response = await self.receive_response()
        return response

    async def send_request(self, request):
        self.writer.write(json.dumps(request).encode('utf-8'))
        print('send a request: {}'.format(json.dumps(request).encode('utf-8')))
        await self.writer.drain()

    async def receive_response(self):
        data = await self.reader.read(4096)
        print('received a response: {}'.format(data))
        response = json.loads(data.decode('utf-8'))
        return response
