from rest_framework.test import APITestCase
from django.core.files import File
import os

from service.fixtues import TestProfileFixture, TestPostFixture
from profiles.models import Post


class TestProfileModel(TestProfileFixture, APITestCase):

    def test_default_null(self):
        profile = self.user_account.profile
        self.assertEqual(profile.status, None)
        self.assertEqual(profile.bio, None)
        self.assertEqual(profile.sex, "Не выбран")
        self.assertEqual(profile.photo, None)
        self.assertEqual(profile.birthday, None)

    def test_create(self):
        with open("profiles/tests/data/image.jpg", 'rb') as file:
            self.user_pofile.photo = File(file, name='image.jpg')
            self.user_pofile.save()
        self.assertEqual(self.user_pofile.photo.url, '/media/uploads/profile_img/image.jpg')
        if os.path.exists("media/uploads/profile_img/image.jpg"):
            os.remove("media/uploads/profile_img/image.jpg")
            self.user_pofile.photo = None
            self.user_pofile.save()


class TestPostModel(TestPostFixture):
    def test_default(self):
        self.assertEqual(self.user_post.text, None)
        self.assertEqual(self.user_post.photo, None)
        self.assertNotEqual(self.user_post.time_created, None)
        self.assertNotEqual(self.user_post.time_updated, None)

    def test_create(self):
        with open("profiles/tests/data/image.jpg", 'rb') as file:
            new_post = Post.objects.create(
                text="I am writing tests for Post model.",
                photo=File(file, name='image.jpg'),
                profile=self.user_pofile
            )
        self.assertEqual(new_post.photo.url, '/media/uploads/post_img/image.jpg')
        self.assertEqual(new_post.text, "I am writing tests for Post model.")
        self.assertEqual(len(Post.post_manager.all_by_username(self.user.username)), 2)
        if os.path.exists("media/uploads/post_img/image.jpg"):
            os.remove("media/uploads/post_img/image.jpg")
