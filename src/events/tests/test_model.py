from datetime import datetime, timedelta

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
            event_start_time=datetime.now() + timedelta(hours=4),
            event_end_time=datetime.now() + timedelta(hours=6)
        )
        self.assertTrue(Event.objects.filter(title="Event_1_title").exists())
        self.assertTrue(Group.objects.filter(title="Event_1_title").exists())
