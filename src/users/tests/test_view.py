from rest_framework.test import APITestCase
from django.urls import reverse
from http import HTTPStatus

from users.models import Account
from service.fixtues import TestAccountFixture


class TestAccountView(TestAccountFixture, APITestCase):

    # def test_account_create(self):
    #     data = {
    #         "region_name": self.city1.region.name,
    #         "city_name": self.city1.name,
    #         "user": {
    #             "username": "asdoaipodija",
    #             "password": "super_mouser9100",
    #             "first_name": "Snoop",
    #             'last_name': "Dogg",
    #             "email": "mokky@mail.ru"
    #         }
    #     }
    #     response = self.client.post(path=reverse("accounts"), data=data, format='json')
    #     self.assertEqual(response.status_code, 201)
    #     user_data = data['user']
    #     user_data.pop("password")
    #     data['user'] = user_data
    #     self.assertEqual(response.json(), data)

    def test_account_create_fail(self):
        data = {
            "region_name": self.city1.region.name,
            "city_name": self.city1.name,
            "user": {
                "username": "asdoaipodija",
                "password": "super_mouser9100",
            }
        }
        response = self.client.post(path=reverse("accounts"), data=data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json(), {'user': {'first_name': ['This field is required.'],
                                           'last_name': ['This field is required.']}})

    def test_account_retrieve(self):
        response = self.user_client.get(reverse("accounts_me"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {
            "city_name": self.city1.name,
            "region_name": self.city1.region.name,
            "user": {
                "username": self.user.username,
                "email": self.user.email,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name
            }
        })

    def test_account_deactivate(self):
        response = self.user_client.delete(reverse("accounts_me"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"detail": "User deactivated."})
        self.user.refresh_from_db()
        self.assertEqual(self.user.is_active, False)

    def test_account_delete(self):
        pre_accounts_count = Account.objects.count()
        response = self.user_client.delete(reverse("accounts_me"), {"delete": True})
        self.assertEqual(response.json(), {"detail": "User deleted."})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(pre_accounts_count - Account.objects.count(), 1)

    def test_account_update(self):
        partial_data = {
            "user": {
                "first_name": "Mick",
                "last_name": "Jagger"
            }
        }
        response = self.user_client.patch(reverse("accounts_me"), data=partial_data, format='json')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, partial_data['user']['last_name'])
        self.assertEqual(self.user.first_name, partial_data['user']['first_name'])


class TestBlockUserViews(TestAccountFixture, APITestCase):

    def test_block_user(self):
        response = self.user_client.post(
            path=reverse("black_list"),
            data={"username": self.user3.username}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"detail": "User blocked successfully."})
        self.user_account.refresh_from_db()
        self.assertTrue(self.user_account.black_list.filter(user=self.user3).exists())

    def test_block_user_fail_yourself(self):
        response = self.user_client.post(
            path=reverse("black_list"),
            data={"username": self.user.username}
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json(), {"detail": "You cannot add yourself to a black list"})

    def test_block_user_fail_not_found(self):
        response = self.user_client.post(
            path=reverse("black_list"),
            data={"username": "a[sdkasdolas"}
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_unblock_user(self):
        response = self.user_client.post(
            path=reverse("black_list"),
            data={"username": self.user3.username}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"detail": "User blocked successfully."})
        self.user_account.refresh_from_db()
        self.assertTrue(self.user_account.black_list.filter(user=self.user3).exists())

        response_delete = self.user_client.delete(
            path=reverse("black_list"),
            data={"username": self.user3.username}
        )
        self.assertEqual(response_delete.status_code, HTTPStatus.OK)
        self.assertEqual(response_delete.json(), {"detail": "User unblocked successfully."})
        self.user_account.refresh_from_db()
        self.assertFalse(self.user_account.black_list.filter(user=self.user3).exists())

    def test_unblock_user_fail_yourself(self):
        response = self.user_client.delete(
            path=reverse("black_list"),
            data={"username": self.user.username}
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.json(), {"detail": "You cannot remove yourself from a black list"})

    def test_unblock_user_fail_not_found(self):
        response = self.user_client.delete(
            path=reverse("black_list"),
            data={"username": "a[sdkasdolas"}
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_blask_list_list(self):
        response = self.user_client.post(
            path=reverse("black_list"),
            data={"username": self.user3.username}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json(), {"detail": "User blocked successfully."})
        self.user_account.refresh_from_db()
        self.assertTrue(self.user_account.black_list.filter(user=self.user3).exists())
        response_list = self.user_client.get(path=reverse("black_list"))
        self.assertEqual(response_list.status_code, HTTPStatus.OK)
        self.assertEqual(
            len(response_list.json()),
            self.user_account.black_list.count()
        )
        self.assertIn(
            self.user3.username,
            [i['user']['username'] for i in response_list.json()]
        )
