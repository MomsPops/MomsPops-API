from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.conf import settings
from django.urls import path

from chats.consumers import ChatConsumer
from chats.models import Chat, Message
from chats.serializers import MessageSerializer
from service.fixtues import TestChatGroupFixture


class ChatConsumerTest(TestChatGroupFixture):
    """
    Tests for Cchat consumer.
    """

    @database_sync_to_async
    def chat_exists(self, chat_id):
        return Chat.objects.filter(id=chat_id).exists()

    @database_sync_to_async
    def messages_count(self):
        return Message.objects.all().count()

    @database_sync_to_async
    def serialize_message(self):
        return MessageSerializer(self.message).data

    async def test_chat_consumer(self):
        """
        Chat consumer tests.
        """
        # Changing channels layers settings for tests
        settings.CHANNEL_LAYERS = {
            'default': {
                'BACKEND': 'channels.layers.InMemoryChannelLayer',
            },
        }

        # Creating an application for testing keyword arguments in the scope
        application = URLRouter([
            path("ws/chats/<uuid:chat_id>/", ChatConsumer.as_asgi()),
        ])

        # Not authenticated user can't connect to channel test
        communicator_anon = WebsocketCommunicator(application, f"ws/chats/{self.simple_chat.id}/")
        connected_anon, _ = await communicator_anon.connect()
        self.assertFalse(connected_anon)

        # Adding headers for authenticate user
        headers = [(b'origin', b'...'), (b'cookie', self.user_client.cookies.output(header='', sep='; ').encode())]
        communicator = WebsocketCommunicator(application, f"ws/chats/{self.simple_chat.id}/", headers)

        # TODO How to authenticate user correctly in channels testing?
        communicator.scope['user'] = self.user
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        self.assertEquals(await self.messages_count(), 1)

        # Message sending test
        await communicator.send_json_to({
            "type": "chat_message",
            "message": await self.serialize_message(),
        })
        response = await communicator.receive_json_from()
        self.assertTrue(response)
        self.assertEquals(await self.messages_count(), 2)

        # Tests should end with disconnecting
        await communicator.disconnect()
