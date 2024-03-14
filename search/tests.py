from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from django.urls import reverse


class TestSearch(APITestCase):
    """
    Test case for the search API view.
    """

    def setUp(self):
        """
        This method is called before each test.
        """

        self.username = "octoTest"
        self.password = "test1234"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        self.token = self.get_auth_token()

    @patch("search.api.Search.execute")
    def test_elasticsearch_query(self, mocked_execute):
        """
        Test the elasticsearch query.
        """

        query_data = {"query": "Hostname = octoxlabs*"}
        expected_response = [{"hostname": "octoxlabs01", "ip_addresses": ["0.0.0.0"]}]

        # Mocking the Elasticsearch client and search results
        mocked_execute.return_value = [
            {"hostname": "octoxlabs01", "ip_addresses": ["0.0.0.0"]}
        ]

        url = reverse("search")
        self.client.credentials(HTTP_AUTHORIZATION=f"Octoxlabs {self.token}")
        response = self.client.post(url, query_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_response)

    def get_auth_token(self):
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"username": self.username, "password": self.password}, format="json"
        )
        return response.data["access"]
