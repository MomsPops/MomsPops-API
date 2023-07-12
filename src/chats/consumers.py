from asgiref.sync import async_to_sync

from channels.generic.websocket import JsonWebsocketConsumer


class ChatConsumer(JsonWebsocketConsumer):
    """
    Consumer for chats.
    """
    def connect(self):
        """Сonnection to websocket."""

        if self.scope["user"].is_anonymous:
            self.close()
        else:
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = "chat_%s" % self.room_name

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )

            self.accept()

    def disconnect(self, close_code):
        """Disconnecting from websocket."""

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
