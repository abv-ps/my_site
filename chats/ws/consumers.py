import json
from datetime import datetime

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chats.ws.constants import GROUP_ADMIN, GROUP_USER
from chats.ws.utils import get_user_details


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        user = self.scope["user"]

        print(f"User from scope: {user} (is_authenticated: {user.is_authenticated}) Type: {type(user)}")

        if user.is_anonymous:
            print("Anonymous user tried to connect")
            await self.close()
            return
        print(f"User {user.username} connected")
        await self.channel_layer.group_add(self.group_name, self.channel_name)

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
        try:
            if content:
                user = self.scope["user"]

                user_details = await get_user_details(user.id)

                if user_details:
                    response = {
                        'response': 'Successfully retrieved the data',
                        'user_details': user_details
                    }
                else:
                    response = {'error': 'User not found'}

                await self.send_json(response)

                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'chat_message',
                        'message': f'Successfully retrieved the data from {user.username}'
                    }
                )
            else:
                await self.send_json({'error': 'Received empty message'})
        except json.JSONDecodeError:
            await self.send_json({'error': 'Invalid JSON received'})

    async def send_json(self, content, close=False):
        await self.send(text_data=json.dumps(content))

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'tweet': event['message']
        }))

    async def user_joined(self, event):
        username = event["username"]
        joined_at = event["joined_at"]
        await self.send_json({
            "type": "user_joined",
            "username": username,
            "joined_at": joined_at,
        })
