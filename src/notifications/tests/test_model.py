
from datetime import datetime
from uuid import UUID

from django.test import TestCase

from ..models import Notification


class NotificationModelTest(TestCase):
    """
    Notification model tests.
    """

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.notifctn = Notification.objects.create(
            text='some text',
            links='https://example.com'
        )

    def test_notification_fields_types(self):
        """
        Correctness of field's types test.
        """

        self.assertIsInstance(self.notifctn.text, str)
        self.assertIsInstance(self.notifctn.links, str)
        self.assertIsInstance(self.notifctn.time_created, datetime)
        self.assertIsInstance(self.notifctn.is_active, bool)
        self.assertIsInstance(self.notifctn.id, UUID)

    def test_notification_object_cretation(self):
        """
        Correctness of notification creation.
        """

        note = Notification.objects.create(
            text='text',
            links='https://youtube.com',
        )
        notifications = Notification.objects.all()
        self.assertEqual(len(notifications), 2)
        self.assertIs(note.is_active, True)
        self.assertIsNotNone(note.time_created)

    def test_deactivate_method(self):
        """
        Deactivate method test.
        """

        note_2 = Notification.objects.create(
            text='another text',
            links='https://yandex.ru',
        )
        self.assertEqual(note_2.is_active, True)
        note_2.deactivate()
        self.assertEqual(note_2.is_active, False)
