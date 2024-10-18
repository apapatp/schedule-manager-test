from rest_framework.test import APITestCase
from schedule_manager.models import User


class UserModelAndManagerTestCase(APITestCase):
    """
    Test the user model and manager.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.basic_user = User.objects.create_user(
            email="test_user@gmail.com",
            password="test_password",
        )
        cls.superuser = User.objects.create_superuser(
            email="superuser@gmail.com",
            password="superuser_password",
        )

    def test_get_created_basic_user(self):
        """
        Test the created basic user.
        """

        user = User.objects.get(email=self.basic_user.email)
        self.assertEqual(user.email, self.basic_user.email)
        self.assertFalse(user.is_superuser)

    def test_get_created_superuser(self):
        """
        Test the created superuser.
        """

        user = User.objects.get(email=self.superuser.email)
        self.assertEqual(user.email, self.superuser.email)
        self.assertTrue(user.is_superuser)

    def test_create_basic_user_with_raises_error(self):
        """
        Test creating a basic user with missing email and password.
        """

        payloads = [
            {"email": "", "password": "test_password"},
            {"email": "basic_user@gmail.com", "password": ""},
        ]

        for payload in payloads:
            with self.assertRaises(ValueError):
                User.objects.create_user(**payload)

    def test_create_superuser_with_raises_error(self):
        """
        Test creating a superuser with missing email and password.
        """

        payloads = [
            {"email": "", "password": "superuser_password"},
            {"email": "superuser@gmail.com", "password": ""}
        ]

        for payload in payloads:
            with self.assertRaises(ValueError):
                User.objects.create_superuser(**payload)
