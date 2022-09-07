import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self):
        pass

    async def receive(self, text_data):
        data=json.loads(text_data)
        message = data['message']
        sender = data['sender']
        receiver = data['receiver']

        await self.save_message(sender, receiver, message)

        await self.channel_layer.send(
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'receiver': receiver
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        print('chat_msg fn is called')
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver
        }))
        print('chat_msg fn is executed')

    @sync_to_async
    def save_message(self, sender, receiver, message):
        print('csave msg called')
        Message.objects.create(sender=sender, receiver=receiver, message=message)
        print('save msg executed')

