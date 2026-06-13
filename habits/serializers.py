from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "periodicity",
            "reward",
            "time_to_execute",
            "is_public",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user"]

    def validate_related_habit(self, value):
        if value and not value.is_pleasant:
            raise serializers.ValidationError(
                "В связанные привычки могут попадать только привычки с признаком приятной привычки."
            )
        return value

    def validate(self, data):
        if data.get("related_habit") and data.get("reward"):
            raise serializers.ValidationError(
                "Нельзя одновременно выбрать связанную привычку и указать вознаграждение."
            )

        if data.get("is_pleasant") and (data.get("reward") or data.get("related_habit")):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        periodicity = data.get("periodicity", 1)
        if periodicity < 1 or periodicity > 7:
            raise serializers.ValidationError(
                "Нельзя выполнять привычку реже, чем 1 раз в 7 дней."
            )

        time_to_execute = data.get("time_to_execute")
        if time_to_execute > 120:
            raise serializers.ValidationError(
                "Время выполнения должно быть не больше 120 секунд."
            )

        return data
    
    
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "password2"]

    def validate_password2(self, value):
        data = self.initial_data
        if data.get("password") != value:
            raise serializers.ValidationError("Passwords do not match.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )