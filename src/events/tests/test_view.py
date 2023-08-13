from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APITestCase

from service.fixtues import TestEventsFixture

from ..models import Event


class TestEventView(TestEventsFixture, APITestCase):

    def test_events_list(self):
        response = self.user_client.get(reverse("events-list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), len(Event.objects.all()))

    def test_events_filter(self):
        response = self.user_client.get(reverse("events-list") + "?title=first")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), len(Event.objects.filter(title__contains="first")))
        response_2 = self.user_client.get(reverse("events-list") + "?description=first")
        self.assertEqual(len(response_2.json()), len(Event.objects.filter(description__contains="first")))
        response_3 = self.user_client.get(reverse("events-list") + "?owner=mi123achael7123")
        self.assertEqual(len(response_3.json()),
                         len(Event.objects.filter(creator__user__username__contains="mi123achael7123")))
        response_4 = self.user_client.get(reverse("events-list") + "?is_active=1")
        self.assertEqual(len(response_4.json()), len(Event.objects.all()))
        response_5 = self.user_client.get(reverse("events-list") + "?is_ongoing=1")
        self.assertEqual(len(response_5.json()), len(Event.objects.none()))

    def test_event_get_one(self):
        response = self.user_client.get(reverse("events-detail", kwargs={"pk": self.event1.id}))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_event_delete(self):
        self.assertTrue(Event.objects.filter(pk=self.event2.id).exists())
        response = self.user_client.delete(reverse("events-detail", kwargs={"pk": self.event1.id}))
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
        response_2 = self.user3_client.delete(reverse("events-detail", kwargs={"pk": self.event2.id}))
        self.assertEqual(response_2.status_code, HTTPStatus.NO_CONTENT)
        self.assertFalse(Event.objects.filter(pk=self.event2.id).exists())
