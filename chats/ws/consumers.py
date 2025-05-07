import json
from datetime import datetime

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from channels.db import database_sync_to_async

from chats.ws.constants import GROUP_ADMIN, GROUP_USER
from chats.ws.utils import get_user


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        user = self.scope["user"]

        if user.is_anonymous:
            await self.close()
        else:
            if user.is_superuser:
                await self.channel_layer.group_add(GROUP_ADMIN, self.channel_name)

            await self.channel_layer.group_add(GROUP_USER, self.channel_name)
            await self.accept()

            await self.channel_layer.group_send(
                GROUP_USER,
                {
                    'type': 'user_joined',
                    'username': user.username,
                    'joined_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        await self.send_json({'response': 'Successfully retrieved the data'})
        user = self.scope["user"]
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': f'Successfully retrieved the data from {user.username}'
            }
        )
    async def send_json(self, content, close=False):
        await self.send(text_data=json.dumps(content))

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
