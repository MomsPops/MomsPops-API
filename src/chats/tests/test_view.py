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

    def test_standart_chat_creates(self):
        response = self.user3_client.post(
            reverse("chats-create_stnd_chat", kwargs={"account_id": self.user2_account.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Chat.objects.filter(members__in=[self.user2_account, self.user3_account]))

    def test_leave_chat(self):
        response = self.user_client.post(
            reverse("chats-leave_chat", kwargs={"pk": self.simple_chat.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.data, "You can't leave personal chat.")

    def test_create_custom_chat(self):
        response = self.user_client.post(
            reverse("chats-create_custom_chat",
                    kwargs={"account_ids": [str(self.user2_account.id), str(self.user3_account.id)]})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(Chat.chat_manager.filter(
            type="CSTM",
            members__in=[self.user2_account, self.user_account, self.user3_account]).exists()
        )
