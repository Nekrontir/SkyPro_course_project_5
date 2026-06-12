from django.urls import path
from .views import (
    HabitListCreateView,
    HabitDetailView,
    PublicHabitListView,
)

urlpatterns = [
    path("habits/", HabitListCreateView.as_view(), name="habits-list-create"),
    path("habits/<int:pk>/", HabitDetailView.as_view(), name="habit-detail"),
    path("habits/public/", PublicHabitListView.as_view(), name="public-habits"),
]