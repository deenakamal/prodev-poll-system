from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class UsersAPITest(TestCase):
    """
    Test suite for Users API (registration, profile).
    """

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.profile_url = reverse("user-profile")

        # Create a user for authentication tests
        self.user = User.objects.create_user(
            username="tester",
            email="tester@example.com",
            password="testpass123"
        )

    def test_register_user_success(self):
        """
        Ensure a new user can register successfully.
        """
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass123"
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_user_duplicate_username(self):
        """
        Ensure duplicate usernames are not allowed.
        """
        payload = {
            "username": "tester",  # already exists
            "email": "another@example.com",
            "password": "anotherpass123"
        }
        response = self.client.post(self.register_url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_profile_authenticated(self):
        """
        Ensure authenticated user can get their profile.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "tester")
        self.assertEqual(response.data["email"], "tester@example.com")

    def test_update_user_profile(self):
        """
        Ensure user can update their profile fields.
        """
        self.client.force_authenticate(user=self.user)
        payload = {"first_name": "John", "last_name": "Doe"}
        response = self.client.patch(self.profile_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")

    def test_profile_requires_authentication(self):
        """
        Ensure profile cannot be accessed without authentication.
        """
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
