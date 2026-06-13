from django.urls import path

from .views import (
    HabitDetailView,
    HabitListCreateView,
    PublicHabitListView,
    UserRegistrationView,
)

urlpatterns = [
    path("habits/", HabitListCreateView.as_view(), name="habits-list-create"),
    path("habits/<int:pk>/", HabitDetailView.as_view(), name="habit-detail"),
    path("habits/public/", PublicHabitListView.as_view(), name="public-habits"),
    path("auth/register/", UserRegistrationView.as_view(), name="auth-register"),
]
