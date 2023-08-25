from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from chats.models import Group
from service.fixtues import TestEventsFixture

from ..models import Event


class TestEvents(TestEventsFixture, APITestCase):

    def test_event_creation(self):
        Event.objects.create(
            title="Event_1_title",
            description="Event_1_description",
            creator=self.user_account,
            time_started=timezone.now() + timedelta(hours=4),
            time_finished=timezone.now() + timedelta(hours=6)
        )
        self.assertTrue(Event.objects.filter(title="Event_1_title").exists())
        self.assertTrue(Group.objects.filter(title="Event_1_title").exists())
