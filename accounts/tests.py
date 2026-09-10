from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AuthenticationAPITests(APITestCase):

    def test_user_registration(self):
        url = reverse("register")

        data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "Password123!",
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            User.objects.filter(
                email="test@example.com"
            ).exists()
        )

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(
            email="test@example.com",
            name="Existing User",
            password="Password123!",
        )

        url = reverse("register")

        data = {
            "name": "Another User",
            "email": "test@example.com",
            "password": "Password123!",
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_login_returns_tokens(self):
        User.objects.create_user(
            email="login@example.com",
            name="Login User",
            password="Password123!",
        )

        url = reverse("login")

        data = {
            "email": "login@example.com",
            "password": "Password123!",
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_login_is_rejected(self):
        User.objects.create_user(
            email="login@example.com",
            name="Login User",
            password="Password123!",
        )

        url = reverse("login")

        data = {
            "email": "login@example.com",
            "password": "WrongPassword123!",
        }

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_me_requires_authentication(self):
        url = reverse("me")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_refresh_token(self):
        register_response = self.client.post(
            reverse("register"),
            {
                "name": "Refresh User",
                "email": "refresh@example.com",
                "password": "strongpassword123",
            },
            format="json",
        )

        self.assertEqual(register_response.status_code, 201)

        login_response = self.client.post(
            reverse("login"),
            {
                "email": "refresh@example.com",
                "password": "strongpassword123",
            },
            format="json",
        )

        self.assertEqual(login_response.status_code, 200)

        refresh_token = login_response.data["refresh"]

        response = self.client.post(
            reverse("token_refresh"),
            {
                "refresh": refresh_token,
            },
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)