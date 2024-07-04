import asyncio
import aiofiles
import json

class FileHandler:
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer

    async def send_file(self, sender_id, receiver_id, file_path, file_type='file'):
        async with aiofiles.open(file_path, 'rb') as f:
            file_data = await f.read()
        request = {
            'type': 'send_message',
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'message': file_data.hex(),
            'msg_type': file_type
        }
        await self.send_request(request)
        response = await self.receive_response()
        return response

    async def receive_file(self, file_data, file_path):
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(bytes.fromhex(file_data))

    async def send_request(self, request):
        self.writer.write(json.dumps(request).encode())
        await self.writer.drain()

    async def receive_response(self):
        data = await self.reader.read(100)
        response = json.loads(data.decode())
        return response
