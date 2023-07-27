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
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.json_message = {
            "text": "Hello World!!"
        }

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

        # Not authenticated user can't connect to channel test
        communicator_not_member = WebsocketCommunicator(application, f"ws/chats/{self.simple_chat.id}/")
        communicator_not_member.scope['user'] = self.user3
        communicator_not_member, _ = await communicator_not_member.connect()
        self.assertFalse(communicator_not_member)

        # Adding headers for authenticate user
        headers = [(b'origin', b'...'), (b'cookie', self.user_client.cookies.output(header='', sep='; ').encode())]
        communicator = WebsocketCommunicator(application, f"ws/chats/{self.simple_chat.id}/", headers)

        # TODO How to authenticate user correctly in channels testing?
        communicator.scope['user'] = self.user
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        self.assertEqual(await self.messages_count(), 1)

        # Message sending test
        await communicator.send_json_to({
            "type": "send_message",
            "message": self.json_message,
        })
        response = await communicator.receive_json_from()
        self.assertTrue(response)
        self.assertEqual(await self.messages_count(), 2)

        await communicator.send_json_to({
            "type": "change_message",
            "message": {"id": str(self.message.id),
                        "text": "Hola el Mundo!"},
        })
        response_2 = await communicator.receive_json_from()
        self.assertEqual(response_2["message"]["text"], "Hola el Mundo!")

        await communicator.send_json_to({
            "type": "viewed",
            "message": {"id": str(self.message.id)},
        })
        response_3 = await communicator.receive_json_from()
        self.assertTrue(response_3["message"]["viewed"])

        # Tests should end with disconnecting
        await communicator.disconnect()
