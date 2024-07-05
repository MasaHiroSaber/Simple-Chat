# -- coding: utf-8 --**
import asyncio
import json


class UserHandler:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def connectTest(self):
        request = {
            'type': 'connect'
        }
        await self.send_request(request)
        response = await self.receive_response()
        return response

    async def register(self, username, password, avatar='default_avatar.png'):
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

    async def update_avatar(self, username, avatar_path):
        request = {
            'type': 'update_avatar',
            'username': username,
            'avatar_path': avatar_path
        }
        await self.send_request(request)
        response = await self.receive_response()
        return response

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

    async def send_request(self, request):
        self.writer.write(json.dumps(request).encode('utf-8'))
        print('send a request: {}'.format(json.dumps(request).encode('utf-8')))
        await self.writer.drain()

    async def receive_response(self):
        data = await self.reader.read(1024)
        print('received a response: {}'.format(data))
        response = json.loads(data.decode('utf-8'))
        return response
