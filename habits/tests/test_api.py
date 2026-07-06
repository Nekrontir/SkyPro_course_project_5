from datetime import time

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from habits.models import Habit

User = get_user_model()


class HabitAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="apiuser",
            email="api@example.com",
            password="testpass123",
        )

        # получаем JWT токен: /api/auth/token/
        token_url = reverse("token_obtain_pair")
        response = self.client.post(
            token_url,
            {"username": "apiuser", "password": "testpass123"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        access = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_create_habit(self):
        # /api/habits/ → name="habits-list-create"
        url = reverse("habits-list-create")
        data = {
            "place": "Дом",
            "time": "09:00:00",
            "action": "Сделать зарядку",
            "is_pleasant": False,
            "periodicity": 1,
            "reward": "Кофе",
            "time_to_execute": 60,
            "is_public": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 1)
        habit = Habit.objects.first()
        self.assertEqual(habit.user, self.user)

    def test_list_only_own_habits(self):
        other = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="otherpass123",
        )

        Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(9, 0),
            action="Моя привычка",
            is_pleasant=False,
            periodicity=1,
            reward="Кофе",
            time_to_execute=60,
            is_public=False,
        )

        Habit.objects.create(
            user=other,
            place="Офис",
            time=time(10, 0),
            action="Чужая привычка",
            is_pleasant=False,
            periodicity=1,
            reward="Чай",
            time_to_execute=60,
            is_public=False,
        )

        url = reverse("habits-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["action"], "Моя привычка")

    def test_public_habits_list(self):
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(9, 0),
            action="Публичная",
            is_pleasant=False,
            periodicity=1,
            reward="Кофе",
            time_to_execute=60,
            is_public=True,
        )

        Habit.objects.create(
            user=self.user,
            place="Офис",
            time=time(10, 0),
            action="Приватная",
            is_pleasant=False,
            periodicity=1,
            reward="Чай",
            time_to_execute=60,
            is_public=False,
        )

        url = reverse("public-habits")

        self.client.credentials()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["action"], "Публичная")
