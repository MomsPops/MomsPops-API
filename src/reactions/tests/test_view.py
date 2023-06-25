from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APITestCase

from reactions.views import ReactionItemViewSet
from service.fixtues import TestUserFixture


class TestReactionViewSet(TestUserFixture, APITestCase):

    def test_reaction_(self):
        ReactionItemViewSet.permission_classes = []
        response = self.user_client.get(
            reverse("reaction_create"))
        assert response.status_code == HTTPStatus.OK
