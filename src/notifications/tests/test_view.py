from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APITestCase

from notifications.models import Notification, NotificationAccount
from service.fixtues import TestAccountFixture


class TestNotifications(TestAccountFixture, APITestCase):
    """
    Notifications tests.
    """

    @ classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ntfctn_1 = Notification.objects.create(
            text='text',
            links='https://example.com',
        )
        cls.ntfctn_1.account.add(cls.user_account)

    def test_get_all_notifications(self):
        """All notifications receiving test."""

        response = self.user_client.get(
            reverse("get_notifications")
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_one_notification(self):
        """One notification receiving test."""

        prsnl_ntfct = NotificationAccount.objects.get(
            notification=self.ntfctn_1
        )
        response = self.user_client.get(
            reverse("get_notification", kwargs={'pk': prsnl_ntfct.id})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json()['viewed'], False)

    def test_change_notification(self):
        """Notification is viewed test."""

        prsnl_ntfct = NotificationAccount.objects.get(
            notification=self.ntfctn_1
        )
        response_1 = self.user_client.post(
            reverse("change_notification", kwargs={'pk': prsnl_ntfct.id})
        )
        self.assertEqual(response_1.status_code, HTTPStatus.OK)

        response_2 = self.user_client.get(
            reverse("get_notification", kwargs={'pk': prsnl_ntfct.id})
        )
        self.assertEqual(response_2.json()['viewed'], True)
