from django.urls import reverse
from rest_framework.test import APITestCase

from profiles.models import Post, Profile
from service.fixtues import TestProfileFixture, TestPostFixture


class TestProfileViews(TestProfileFixture, APITestCase):
    def test_profile_detail(self):
        response = self.user_client.get(
            reverse("profiles_detail", kwargs={'username': self.user_account.user.username})
        )
        self.assertEqual(response.status_code, 200)

    def test_profile_detail_fail(self):
        response = self.user_client.get(
            reverse("profiles_detail", kwargs={'username': "postgres"})
        )
        self.assertEqual(response.status_code, 404)

    def test_profile_list(self):
        response = self.user_client.get(reverse("profiles"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), len(Profile.profile_manager.all()))

    def test_profile_update(self):
        data_update = {"bio": "I was born tomorrow."}
        response = self.user_client.patch(
            reverse("profiles_detail", kwargs={'username': self.user_account.user.username}), data=data_update
        )
        self.assertEqual(response.status_code, 200)
        self.user_pofile.refresh_from_db()
        self.assertEqual(self.user_pofile.bio, data_update['bio'])

    def test_profile_update_other_fail(self):
        data_update = {"bio": "I was born tomorrow and today."}
        response = self.superuser_client.patch(
            reverse("profiles_detail", kwargs={'username': self.user_account.user.username}), data=data_update
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})
        self.user_pofile.refresh_from_db()

    def test_profile_posts(self):
        response = self.user_client.get(
            reverse("profiles_posts", kwargs={'username': self.user_account.user.username})
        )
        self.assertEqual(response.status_code, 200)


class TestPostView(TestPostFixture, APITestCase):

    def test_list_on_profile(self):
        response = self.user_client.get(
            reverse("profiles_posts", kwargs={'username': self.user_account.user.username})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), len(Post.post_manager.all_by_username(self.user.username)))

    def test_post_create(self):
        post_count_before = len(Post.post_manager.all_by_username(self.user.username))
        post_data = {
            "text": "Python is better han Javascript, really."
        }
        response = self.user_client.post(reverse("posts"), data=post_data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['text'], post_data['text'])
        self.user_pofile.refresh_from_db()
        self.assertEqual(len(Post.post_manager.all_by_username(self.user.username)) - post_count_before, 1)

    def test_post_retrieve(self):
        response = self.user_client.get(
            reverse("posts_detail", kwargs={'id': self.superuser_post.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_post_update(self):
        data_update = {"text": "I was born tomorrow."}
        response = self.user_client.patch(
            reverse("posts_detail", kwargs={'id': self.user_post.id}), data=data_update
        )
        self.assertEqual(response.status_code, 200)
        self.user_post.refresh_from_db()
        self.assertEqual(self.user_post.text, data_update['text'])

    def test_post_update_other_fail(self):
        data_update = {"text": "I was born tomorrow and today."}
        response = self.superuser_client.patch(
            reverse("posts_detail", kwargs={'id': self.user_post.id}), data=data_update
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

    def test_post_delete(self):
        post_count_before = len(Post.post_manager.all_by_username(self.user.username))
        response = self.user_client.delete(
            reverse("posts_detail", kwargs={"id": self.user_post.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Post.post_manager.all_by_username(self.user.username)) - post_count_before, -1)

    def test_post_delete_other_fail(self):
        response = self.superuser_client.delete(
            reverse("posts_detail", kwargs={"id": self.user_post.id})
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})
