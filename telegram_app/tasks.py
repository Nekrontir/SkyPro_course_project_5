import requests
from celery import shared_task
from django.conf import settings
# from django.utils import timezone

from habits.models import Habit


@shared_task
def send_habit_reminders():
    """
    Отправить уведомления в Telegram о привычках, которые нужно выполнить сегодня.
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return

    # today = timezone.now().date()

    habits = Habit.objects.all()

    chat_id = settings.CHAT_ID

    for habit in habits:
        message = (
            f"Привет! Не забудь выполнить привычку:\n"
            f"{habit.action}\n"
            f"Время: {habit.time}\n"
            f"Место: {habit.place}"
        )

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
        }

        try:
            requests.post(url, data=data)
        except Exception:
            pass
