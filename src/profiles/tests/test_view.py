from http import HTTPStatus

from django.urls import reverse
from rest_framework.test import APITestCase

from profiles.models import Post, Profile
from service.fixtues import TestProfileFixture, TestPostFixture
from users.models import Account


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

    def test_profile_friends_both_side(self):
        response = self.user2_client.get(
            reverse("profiles_friends", kwargs={'username': self.superuser_account.user.username})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        account3_data = data[0]
        self.assertEqual(account3_data['user']['username'], self.user3_account.user.username)

    def test_profile_friends(self):
        response = self.user_client.get(
            reverse("profiles_friends", kwargs={'username': self.user3_account.user.username})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        account3_data = data[0]
        self.assertEqual(account3_data['city_name'], self.superuser_account.city.name)

    def test_profile_fail_unauthorized(self):
        response = self.client.get(
            reverse("profiles_friends", kwargs={'username': self.user3_account.user.username})
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        data = response.json()
        self.assertIn('detail', data)

    def test_profile_friend_delete_fail(self):
        account1_friends_amount_before = len(self.user_account.friends.all())
        all_accounts_friends_amount_before = sum(a.friends.count() for a in Account.objects.all())
        response = self.user_client.delete(
            reverse("profiles_friend_delete", kwargs={'username': self.user3_account.user.username})
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        data = response.json()
        self.assertIn('detail', data)
        self.assertEqual(data['detail'], f"Account {self.user3_account} is not your friend.")
        self.user_account.refresh_from_db()
        account1_friends_after = self.user_account.friends.all()
        all_accounts_friends_amount_after = sum(a.friends.count() for a in Account.objects.all())
        self.assertEqual(len(account1_friends_after), account1_friends_amount_before)
        self.assertEqual(all_accounts_friends_amount_after, all_accounts_friends_amount_before)

    def test_profile_friend_fail_yourself(self):
        account1_friends_amount_before = len(self.user_account.friends.all())
        all_accounts_friends_amount_before = sum(a.friends.count() for a in Account.objects.all())
        response = self.user_client.delete(
            reverse("profiles_friend_delete", kwargs={'username': self.user_account.user.username})
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        data = response.json()
        self.assertIn('detail', data)
        self.assertEqual(data['detail'], "Cannot delete yourself from friends.")
        self.user_account.refresh_from_db()
        account1_friends_after = self.user_account.friends.all()
        all_accounts_friends_amount_after = sum(a.friends.count() for a in Account.objects.all())
        self.assertEqual(len(account1_friends_after), account1_friends_amount_before)
        self.assertEqual(all_accounts_friends_amount_after, all_accounts_friends_amount_before)

    def test_profile_friend_fail_unauthorized(self):
        all_accounts_friends_amount_before = sum(a.friends.count() for a in Account.objects.all())
        response = self.client.delete(
            reverse("profiles_friend_delete", kwargs={'username': self.user2_account.user.username})
        )
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
        data = response.json()
        self.assertIn('detail', data)
        self.user_account.refresh_from_db()
        all_accounts_friends_amount_after = sum(a.friends.count() for a in Account.objects.all())
        self.assertEqual(all_accounts_friends_amount_after, all_accounts_friends_amount_before)

    def test_profile_friend_success(self):
        self.assertIn(self.user3_account, self.superuser_account.friends.all())
        self.assertIn(self.superuser_account, self.user3_account.friends.all())
        all_accounts_friends_amount_before = sum(a.friends.count() for a in Account.objects.all())
        response = self.user3_client.delete(
            reverse("profiles_friend_delete", kwargs={'username': self.superuser_account.user.username})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        data = response.json()
        self.assertIn('detail', data)
        self.assertEqual(data['detail'], "Friendship is broken successfully.")
        self.user_account.refresh_from_db()
        all_accounts_friends_amount_after = sum(a.friends.count() for a in Account.objects.all())
        self.assertEqual(all_accounts_friends_amount_before - all_accounts_friends_amount_after, 2)
        self.assertNotIn(self.user3_account, self.superuser_account.friends.all())
        self.assertNotIn(self.superuser_account, self.user3_account.friends.all())


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
