from datetime import time

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from habits.models import Habit

User = get_user_model()


class HabitModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )

    def test_habit_valid(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(9, 0),
            action="Сделать зарядку",
            is_pleasant=False,
            related_habit=None,
            periodicity=1,
            reward="Кофе",
            time_to_execute=60,
            is_public=True,
        )

        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(habit.user, self.user)

    def test_habit_reward_and_related_forbidden(self):
        pleasant = Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(10, 0),
            action="Принять ванну",
            is_pleasant=True,
            periodicity=1,
            time_to_execute=60,
            is_public=False,
        )

        with self.assertRaises(ValidationError):
            Habit.objects.create(
                user=self.user,
                place="Дом",
                time=time(11, 0),
                action="Сделать зарядку",
                is_pleasant=False,
                related_habit=pleasant,
                periodicity=1,
                reward="Кофе",
                time_to_execute=60,
                is_public=False,
            )
