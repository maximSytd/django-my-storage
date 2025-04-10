import os
from datetime import timedelta

from django.conf import settings

from celery import Celery
import decouple

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

CELERY_TASK_ALWAYS_EAGER = decouple.config(
    "CELERY_TASK_ALWAYS_EAGER",
    default=False,
    cast=bool,
)

app = Celery("my_storage")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    "send_products_notifications": {
        "task": "send_products_notifications",
        "schedule": timedelta(hours=8),
    },
}

app.conf.update(
    timezone='Europe/Moscow',
    enable_utc=True,
    worker_hijack_root_logger=False,
)
