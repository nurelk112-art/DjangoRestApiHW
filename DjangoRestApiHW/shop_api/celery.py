import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop_api.settings")

app = Celery("shop_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "scheduled-task-every-minute": {
        "task": "product.tasks.scheduled_task",
        "schedule": crontab(),
    },
}
