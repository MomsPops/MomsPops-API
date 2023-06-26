from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer


class ChatConsumer(JsonWebsocketConsumer):
    """
    Consumer for chat
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat_id = None

    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = 'chat_%s' % self.chat_id

        # Join to chat
        async_to_sync(self.channel_layer.group_add)(
            self.chat_id,
            self.channel_name,
        )

        self.accept()

        self.send_json(
            {
                "type": "welcome_message",
                "message": "Hey there! You've successfully connected!",
            }
        )

    def disconnect(self, close_code):
        # Leave chat
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "chat_message":
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.chat_id,
                {
                    "type": "chat_message_echo",
                    "name": content["name"],
                    "message": content["message"],
                },
            )
        return super().receive_json(content, **kwargs)

    # Receive message from room group
    def chat_message_echo(self, event):
        self.send_json(event)
