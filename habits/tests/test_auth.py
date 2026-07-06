from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_and_login(self):
        url_register = reverse("auth-register")
        response = self.client.post(
            url_register,
            {
                "username": "newuser",
                "email": "new@example.com",
                "password": "newpass123",
                "password2": "newpass123",
            },
            format="json",
        )

        self.assertIn(response.status_code, (200, 201))
        self.assertTrue(User.objects.filter(username="newuser").exists())
        url_token = reverse("token_obtain_pair")
        response = self.client.post(
            url_token,
            {"username": "newuser", "password": "newpass123"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
