from datetime import timedelta
from http import HTTPStatus

from django.urls import reverse
from django.utils import timezone
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
        response_2 = self.user_client.get(reverse("events-list") + "?owner=mi123achael7123")
        self.assertEqual(len(response_2.json()),
                         len(Event.objects.filter(creator__user__username__contains="mi123achael7123")))
        response_3 = self.user_client.get(reverse("events-list") + "?is_active=1")
        self.assertEqual(len(response_3.json()), len(Event.objects.filter(time_finished__gte=timezone.now())))
        response_4 = self.user_client.get(reverse("events-list") + "?is_ongoing=1")
        self.assertEqual(len(response_4.json()), len(Event.objects.none()))

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

    def test_event_creation(self):
        event_data = {
            "title": "Прогулка в парке",
            "description": "Мы здорово проведем время.",
            "coordinate": {"lat": 20, "lon": 177},
            "time_started": timezone.now() + timedelta(hours=2),
            "time_finished": timezone.now() + timedelta(hours=3),
        }
        response = self.user2_client.post(reverse("events-list"), data=event_data, format="json")
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        event_data_2 = {
            "title": "Прогулка в парке",
            "description": "Мы здорово проведем время.",
            "coordinate": {"lat": 20, "lon": 177},
            "time_started": timezone.now() + timedelta(hours=3),
            "time_finished": timezone.now() + timedelta(hours=2),
        }
        response_2 = self.user2_client.post(reverse("events-list"), data=event_data_2, format="json")
        self.assertEqual(response_2.json(),
                         {'non_field_errors': ['Время завершения не может быть раньше времени начала.']})

        event_data_3 = {
            "title": "Прогулка в парке",
            "description": "Мы здорово проведем время.",
            "coordinate": {"lat": 20, "lon": 177},
            "time_started": timezone.now() - timedelta(hours=3),
            "time_finished": timezone.now() + timedelta(hours=2),
        }
        response_3 = self.user2_client.post(reverse("events-list"), data=event_data_3, format="json")
        self.assertEqual(response_3.json(), {'non_field_errors': ['Время начала должно быть больше текущего.']})

    def test_event_changing(self):
        event_data = {
            "title": "Прогулка",
            "description": "Мы здорово проведем время.",
            "coordinate": {"lat": 42, "lon": 77},
            "time_started": timezone.now() + timedelta(hours=3),
            "time_finished": timezone.now() + timedelta(hours=9),
        }
        response = self.user3_client.put(
            reverse("events-detail", kwargs={"pk": self.event3.id}),
            data=event_data,
            format="json"
        )
        self.assertEqual(response.json(), {"error": "Нельзя изменить прошедшее событие."})

    def test_delete_event(self):
        response = self.user3_client.delete(reverse("events-detail", kwargs={"pk": self.event3.id}))
        self.assertEqual(response.json(), {'error': 'Нельзя удалить прошедшее событие.'})
        response_2 = self.user3_client.delete(reverse("events-detail", kwargs={"pk": self.event2.id}))
        self.assertEqual(response_2.status_code, HTTPStatus.NO_CONTENT)
