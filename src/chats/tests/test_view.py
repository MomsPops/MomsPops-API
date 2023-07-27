from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APITestCase

from chats.models import Chat
from service.fixtues import TestChatGroupFixture


class TestChatView(TestChatGroupFixture, APITestCase):
    """
    Chats tests for views.
    """

    def test_get_all_chats(self):
        """All chats receiving test."""
        response = self.user_client.get(
            reverse("chats-list")
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            len(response.json()),
            len(Chat.chat_manager.get_all_chats_by_account(self.user_account))
        )

    def test_get_one_chat(self):
        """One chat receiving test."""
        response = self.user_client.get(
            reverse("chats-detail", kwargs={"pk": self.simple_chat.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_chat_creates(self):
        response = self.user3_client.post(
            reverse("chats-create_chat", kwargs={"account_id": self.user2_account.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Chat.objects.filter(members__in=[self.user2_account, self.user3_account]))
