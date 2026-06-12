from rest_framework import generics, permissions
from rest_framework.pagination import LimitOffsetPagination
from .models import Habit
from .serializers import HabitSerializer


class HabitPagination(LimitOffsetPagination):
    default_limit = 5


class HabitListCreateView(generics.ListCreateAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(user=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = HabitSerializer

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(user=user).order_by("-created_at")


class PublicHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).order_by("-created_at")