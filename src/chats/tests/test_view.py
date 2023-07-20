from rest_framework.test import APITestCase
from django.urls import reverse
from http import HTTPStatus

from chats.models import Group
from service.fixtues import TestGroupFixture


class TestGroupView(TestGroupFixture, APITestCase):

    def test_groups_list_all(self):
        response = self.user_client.get(reverse("groups"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.json()), len(Group.objects.all()))

    def test_groups_list_filter_title(self):
        response = self.user_client.get(reverse("groups") + "?title=C#")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        print(response.json())
