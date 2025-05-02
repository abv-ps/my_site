from channels.generic.websocket import AsyncJsonWebsocketConsumer

from channels.db import database_sync_to_async


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        data = json.loads(text_data)
        message = data['message']

        username = await self.get_username()

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': f'{username}: {message}'
            }
        )
    async def send_json(self, content, close=False):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))

    @database_sync_to_async
    def get_username(self):
        return self.user.username