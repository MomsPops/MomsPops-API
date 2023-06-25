from django.urls import reverse
from rest_framework.test import APITestCase


class TestAPI(APITestCase):

    def test_docs(self):
        response = self.client.get(reverse("swagger"))
        assert response.status_code == 200
