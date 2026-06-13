from datetime import time
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from habits.models import Habit
from telegram_app.tasks import send_habit_reminders

User = get_user_model()


class SendHabitRemindersTests(TestCase):
    @patch("telegram_app.tasks.requests.post")
    def test_send_habit_reminders(self, mock_post):
        settings.TELEGRAM_BOT_TOKEN = "dummy"
        settings.CHAT_ID = "123456"

        user = User.objects.create_user(
            username="celeryuser",
            email="celery@example.com",
            password="testpass123",
        )

        Habit.objects.create(
            user=user,
            place="Дом",
            time=time(9, 0),
            action="Сделать зарядку",
            is_pleasant=False,
            periodicity=1,
            reward="Кофе",
            time_to_execute=60,
            is_public=True,
        )

        send_habit_reminders()

        self.assertTrue(mock_post.called)
