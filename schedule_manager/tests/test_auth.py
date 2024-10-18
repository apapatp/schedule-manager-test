from django.urls import reverse
from rest_framework import status
from schedule_manager.models import User
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIClient
from schedule_manager.tests.factories import UserFactory


class AuthenticationEndpointTestCases(APITestCase):
    """Registration endpoint test case."""

    def setUp(self) -> None:
        self.client = APIClient()
        self.register_url = reverse("register-user")
        self.login_url = reverse("login-user")
        self.refresh_token_url = reverse("refresh-token")
        self.logout_url = reverse("logout-user")
        self.user_1 = UserFactory()

    def test_register_user_fail(self):
        """Test user registration."""

        payload = {
            "email": "",
            "password": "",
            "first_name": "",
            "last_name": ""
        }

        response = self.client.post(self.register_url, payload, format="json")
        expected_response_data = {
            'email': ['This field may not be blank.'],
            'password': ['This field is required']
        }

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response_data)

    def test_register_user_success_as_patient(self):
        """Test user registration as patient."""

        payload = {
            "email": "senpai@test.com",
            "password": "Senpai@123",
            "first_name": "Senpai",
            "last_name": "Test"
        }

        expected_response_data = {"detail": "Successfully Registered"}
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response_data)

    def test_register_user_success_as_doctor(self):
        """Test user registration as doctor."""

        payload = {
            "email": "senpai@test.com",
            "password": "Senpai@123",
            "first_name": "Senpai",
            "last_name": "Test",
        }

        expected_response_data = {"detail": "Successfully Registered"}
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response_data)

    def test_login_user_fail(self):
        """Test user login."""

        payload = {
            "email": "",
            "password": ""
        }

        response = self.client.post(self.login_url, payload, format="json")
        expected_response_data = {
            'email': ['This field may not be blank.'],
            'password': ['This field may not be blank.']
        }
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, expected_response_data)

    def test_authentication_endpoint_success_is_http_cookie_only_false(self):
        """
        Testing authentication endpoints.
        Register, login, refresh token, and logout with is_http_cookie_only=True.
        """

        payload = {
            "email": "test@test.com",
            "password": "Testing@123"
        }

        # Register the user first
        expected_response_data = {"detail": "Successfully Registered"}
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response_data)

        # Login the user is_http_cookie_only=True
        payload = {
            "email": "test@test.com",
            "password": "Testing@123",
            "is_http_cookie_only": True
        }

        response = self.client.post(self.login_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_expiration", response.data)
        self.assertIn("refresh_expiration", response.data)
        self.assertIn("user", response.data)

        # Rotate the refresh token
        payload = {
            "is_http_cookie_only": True
        }
        response = self.client.post(self.refresh_token_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_expiration", response.data)
        self.assertIn("refresh_expiration", response.data)

        # Logout the user
        payload = {
            "is_http_cookie_only": True
        }
        response = self.client.post(self.logout_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"detail": "Successfully logged out"})

    def test_authentication_endpoint_success_is_http_cookie_only_true(self):
        """
        Testing authentication endpoints.
        Register, login, refresh token, and logout with is_http_cookie_only=False.
        """

        payload = {
            "email": "test@test.com",
            "password": "Testing@123"
        }

        # Register the user first
        expected_response_data = {"detail": "Successfully Registered"}
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_response_data)

        # Login the user is_http_cookie_only=False
        payload = {
            "email": "test@test.com",
            "password": "Testing@123",
        }

        response = self.client.post(self.login_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

        # Rotate the refresh token
        payload = {
            "refresh": response.data["refresh"],
        }
        response = self.client.post(self.refresh_token_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # Logout the user
        self.client.force_authenticate(user=self.user_1)
        payload = {
            "refresh": response.data["refresh"],
        }
        response = self.client.post(self.logout_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"detail": "Successfully logged out"})
