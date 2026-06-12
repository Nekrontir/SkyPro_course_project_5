from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def validate_habit_periodicity(value):
    """Периодичность не больше 7 дней."""
    if value < 1 or value > 7:
        raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")


def validate_habit_time(value):
    """Время выполнения не больше 120 секунд."""
    if value > 120:
        raise ValidationError("Время выполнения должно быть не больше 120 секунд.")


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )

    place = models.CharField(
        max_length=255,
        verbose_name="Место",
    )

    time = models.TimeField(
        verbose_name="Время",
    )

    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
    )

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="related_to",
        verbose_name="Связанная привычка",
    )

    periodicity = models.IntegerField(
        default=1,
        validators=[validate_habit_periodicity],
        verbose_name="Периодичность (в днях)",
    )

    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
    )

    time_to_execute = models.IntegerField(
        validators=[validate_habit_time],
        verbose_name="Время на выполнение (сек)",
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError(
                "Нельзя одновременно выбрать связанную привычку и указать вознаграждение."
            )

        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError(
                "В связанные привычки могут попадать только привычки с признаком приятной привычки."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)