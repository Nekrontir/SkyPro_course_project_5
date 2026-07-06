import os

from celery import Celery
# from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("SkyPro_course_project_5")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
