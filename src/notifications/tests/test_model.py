from datetime import datetime
from uuid import UUID

from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import Account

from ..models import Notification, NotificationAccount

User = get_user_model()


class NotificationModelTest(TestCase):
    """
    Notification model tests.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user1 = User.objects.create_user(
            username='test_user_1',
            password='password_1'
        )
        cls.user2 = User.objects.create_user(
            username='test_user_2',
            password='password_2'
        )
        cls.account1 = Account.objects.create(user=cls.user1)
        cls.account2 = Account.objects.create(user=cls.user2)
        cls.notifctn = Notification.objects.create(
            text='some text',
            link='https://example.com'
        )
        cls.notifctn.accounts.add(cls.account1)

    def test_notification_fields_types(self):
        """
        Correctness of field's types test.
        """

        self.assertIsInstance(self.notifctn.text, str)
        self.assertIsInstance(self.notifctn.link, str)
        self.assertIsInstance(self.notifctn.time_created, datetime)
        self.assertIsInstance(self.notifctn.id, UUID)

    def test_notification_object_cretation(self):
        """
        Correctness of notification creation.
        """

        note = Notification.objects.create(
            text='text',
            link='https://youtube.com',
        )
        note.accounts.add(self.account1, self.account2)
        notifications = Notification.objects.all()
        self.assertEqual(len(notifications), 2)
        self.assertTrue(self.account1.notifications.filter(pk=note.pk).exists())
        self.assertTrue(self.account2.notifications.filter(pk=note.pk).exists())
        self.assertIsNotNone(note.time_created)

    def test_is_viewed_method(self):
        """
        Is_viewed method test.
        """

        note_2 = Notification.objects.create(
            text='another text',
            link='https://yandex.ru',
        )
        note_2.accounts.add(self.account1)
        notification_account = NotificationAccount.objects.get(notification=note_2, account=self.account1)
        self.assertEqual(notification_account.viewed, False)
        notification_account.view()
        self.assertEqual(notification_account.viewed, True)
