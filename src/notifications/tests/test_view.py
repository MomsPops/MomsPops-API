from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from notifications.models import Notification, NotificationAccount
from service.fixtues import TestAccountFixture
from users.models import Account

User = get_user_model()


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
        cls.anonym = APIClient()
        cls.user_2 = User(username='vasya', password='vasya123')
        cls.user_2.set_password('rammqueen123')
        cls.user_2.save()
        cls.user_client_2 = APIClient()
        cls.user_client_2.force_login(cls.user_2)
        cls.user_2_account = Account.objects.create(
            city=cls.city2,
            user=cls.user_2
        )

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

        # User can view personal notification test
        response_1 = self.user_client.get(
            reverse("get_notification", kwargs={'pk': prsnl_ntfct.id})
        )
        self.assertEqual(response_1.status_code, HTTPStatus.OK)
        self.assertEqual(response_1.json()['viewed'], False)

        # User can't view other user's notifications test
        response_2 = self.user_client_2.get(
            reverse("get_notification", kwargs={'pk': prsnl_ntfct.id})
        )
        self.assertEqual(response_2.status_code, HTTPStatus.NOT_FOUND)

    def test_change_notification(self):
        """Notification is viewed test."""

        prsnl_ntfct = NotificationAccount.objects.get(
            notification=self.ntfctn_1
        )

        # User can mark personal notification as viewed
        response_1 = self.user_client.post(
            reverse("change_notification", kwargs={'pk': prsnl_ntfct.id})
        )
        self.assertEqual(response_1.status_code, HTTPStatus.OK)
        response_2 = self.user_client.get(
            reverse("get_notification", kwargs={'pk': prsnl_ntfct.id})
        )
        self.assertEqual(response_2.json()['viewed'], True)

        # User can't change other user's notifications test
        response_3 = self.user_client_2.post(
            reverse("change_notification", kwargs={'pk': prsnl_ntfct.id})
        )
        self.assertEqual(response_3.status_code, HTTPStatus.NOT_FOUND)

    def test_anonym_cant_get_notifications(self):
        """Anonymous user can't view and change notifications test."""

        prsnl_ntfct = NotificationAccount.objects.get(
            notification=self.ntfctn_1
        )

        # Anonymous user can't get notifications list test
        response_1 = self.anonym.get(
            reverse("get_notifications")
        )
        self.assertEqual(response_1.status_code, HTTPStatus.UNAUTHORIZED)

        # Anonymous user can't get one notification test
        response_2 = self.anonym.get(
            reverse("get_notification", kwargs={'pk': prsnl_ntfct.id})
        )
        self.assertEqual(response_2.status_code, HTTPStatus.UNAUTHORIZED)

        # Anonymous user can't change any notifications test
        response_3 = self.anonym.get(
            reverse("change_notification", kwargs={'pk': prsnl_ntfct.id})
        )
        self.assertEqual(response_3.status_code, HTTPStatus.UNAUTHORIZED)
