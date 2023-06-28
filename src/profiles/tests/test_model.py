from rest_framework.test import APITestCase

from service.fixtues import TestProfileFixture, TestPostFixture
from profiles.models import Profile, Post


class TestProfileModel(TestProfileFixture, APITestCase):

    def test_default_null(self):
        profile = self.user_account.profile
        self.assertEqual(profile.status, None)
        self.assertEqual(profile.bio, None)
        self.assertEqual(profile.sex, "Не выбран")
        self.assertEqual(profile.photo, None)
        self.assertEqual(profile.birthday, None)


class TestPostModel(TestPostFixture):
    def test_default(self):
        self.assertEqual(self.user_post.text, None)
        self.assertEqual(self.user_post.photo, None)
        self.assertNotEqual(self.user_post.time_created, None)
        self.assertNotEqual(self.user_post.time_updated, None)
