from rest_framework.test import APITestCase
from django.urls import reverse
from http import HTTPStatus
from random import choice

from notifications.models import NotificationAccount
from service.fixtues import TestNotificationAccountFixture


class TestNotificationView(TestNotificationAccountFixture, APITestCase):
    """
    Notifications tests for views.
    """

    def test_get_all_notifications(self):
        """All notifications receiving test."""
        response = self.user_client.get(
            reverse("notifications")
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            len(response.json()),
            len(NotificationAccount.notification_account_manager.get_all_by_account(self.user_account))
        )

    def test_get_all_notification_fail(self):
        response = self.client.get(
            reverse("notifications")
        )
        self.assertEqual(response.status_code, 401)

    def test_view_notification(self):
        notification = choice(NotificationAccount.notification_account_manager.get_all_by_account(self.user2_account))
        self.assertFalse(notification.viewed)
        response = self.user2_client.post(
            path=reverse("notifications_view", kwargs={"notification_account_id": notification.id}),
        )
        notification.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(notification.viewed)
        self.assertEqual(response.json(), f"Notification {notification.id} viewed.")

    def test_view_notification_already(self):
        notification = choice(NotificationAccount.notification_account_manager.get_all_by_account(self.user2_account))
        self.assertFalse(notification.viewed)
        notification.view()
        notification.refresh_from_db()
        response = self.user2_client.post(
            path=reverse("notifications_view", kwargs={"notification_account_id": notification.id}),
        )
        notification.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(notification.viewed)
        self.assertEqual(response.json(), f"Notification {notification.id} is already viewed.")
