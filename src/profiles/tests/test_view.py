from django.urls import reverse
from rest_framework.test import APITestCase

from service.fixtues import TestProfileFixture


class TestProfileViews(TestProfileFixture, APITestCase):
    def test_profile_detail(self):
        response = self.user_client.get(
            reverse("profiles_detail", kwargs={'username': self.user_account.user.username})
        )
        assert response.status_code == 200

    def test_profile_detail_fail(self):
        response = self.user_client.get(
            reverse("profiles_detail", kwargs={'username': self.superuser.username})
        )
        assert response.status_code == 404

    def test_profile_list(self):
        response = self.user_client.get(reverse("profiles_all"))
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_profile_update(self):
        data_update = {"bio": "I was born tomorrow."}
        response = self.user_client.patch(
            reverse("profiles_update", kwargs={'username': self.user_account.user.username}), data=data_update
        )
        assert response.status_code == 200
        self.user_pofile.refresh_from_db()
        assert self.user_pofile.bio == data_update['bio']
