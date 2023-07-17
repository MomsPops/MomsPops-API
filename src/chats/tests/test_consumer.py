from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.urls import path

from chats.consumers import ChatConsumer
from service.fixtues import TestAccountFixture


class ChatConsumerTest(TestAccountFixture):
    """
    Tests for Cchat consumer.
    """
    async def test_chat_consumer(self):
        application = URLRouter([
            path("ws/chats/<uuid:chat_id>/", ChatConsumer.as_asgi()),
        ])
        communicator = WebsocketCommunicator(application, "ws/chats/3c93bd2f-8f3d-46ef-a732-d897fc94e479/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
