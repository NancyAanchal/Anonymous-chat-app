import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.lobbycode = self.scope['url_route']['kwargs']['lobbycode']
        
        async_to_sync(self.channel_layer.group_add)(
        self.lobbycode,
        self.channel_name
        )

        # async_to_sync(self.update_member_count)()

        self.accept()

        self.send(text_data = json.dumps({
            'type': 'connection_established',
            'message': 'You are connected'
        }))


    # def disconnect(self, close_code):
    #         async_to_sync(self.channel_layer.group_discard)(
    #             self.lobbycode,
    #             self.channel_name
    #         )

    #         async_to_sync(self.update_member_count)()


    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_name = text_data_json['user_name']

        async_to_sync(self.channel_layer.group_send)(
        self.lobbycode,
        {
            'type':'chat_message',
            'message': message,
            'user_name': user_name
        }
        )

        
    def chat_message(self, event):
        message = event['message']
        user_name = event['user_name']
        
        self.send(text_data=json.dumps({
            'type':'chat',
            'message': message,
            'user_name':user_name
        }))


    # async def update_member_count(self, event=None):
    #     # Get the list of channels in the group
    #     channels = await self.channel_layer.group_channels(self.lobbycode)

    #     # Count the number of channels to get the member count
    #     members = len(channels)

    #     # Send a message to update the member count
    #     await self.send(text_data=json.dumps({
    #         'type': 'member_count',
    #         'members': members
    #     }))