# from rest_framework.test import APITestCase
# from django.urls import reverse
# from http import HTTPStatus
#
# from chats.models import Group
# from coordinates.models import Coordinate
#
#
# class TestGroupView(TestGroupFixture, APITestCase):
#
#     def test_groups_list_all(self):
#         response = self.user_client.get(reverse("groups"))
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertEqual(len(response.json()), len(Group.objects.all()))
#
#     def test_groups_list_filter_title(self):
#         response = self.user_client.get(reverse("groups") + "?title=C#")
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         data = response.json()
#         self.assertEqual(len(data), 1)
#         group = data[0]
#         self.assertEqual(
#             group,
#             {
#                 'title': 'C# is better than Python',
#                 'owner': {
#                     'bio': None,
#                     'get_photo_url': '/media/uploads/profile_img/default_avatar.png',
#                     'get_absolute_url': f'/api/v1/profiles/{self.user2_account.user.username}/',
#                     'first_name': '',
#                     'last_name': ''
#                 },
#                 'get_image_preview_url': '/media/uploads/group_img/default_image_preview.png'
#             }
#         )
#
#     def test_groups_filter_distance_3_km(self):
#         Coordinate.coordinate_manager.create(
#             lat=20, lon=20, source=self.user2_account
#         )
#         self.user2_account.refresh_from_db()
#         response = self.user2_client.get(reverse("groups") + "?distance=3000")
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertEqual(len(response.json()), 3)
#
#     def test_groups_filter_distance_1_km(self):
#         Coordinate.coordinate_manager.create(
#             lat=20, lon=20, source=self.user2_account
#         )
#         self.user2_account.refresh_from_db()
#         response = self.user2_client.get(reverse("groups") + "?distance=1000")
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertEqual(len(response.json()), 2)
#
#     def test_groups_filter_distance_100_m(self):
#         Coordinate.coordinate_manager.create(
#             lat=20, lon=20, source=self.user2_account
#         )
#         self.user2_account.refresh_from_db()
#         response = self.user2_client.get(reverse("groups") + "?distance=100")
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertEqual(len(response.json()), 1)
