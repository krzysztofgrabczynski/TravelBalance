from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks(["api.user", "api.currency"])

app.conf.beat_schedule = {
    "fetch-currencies-rates-at-midnight": {
        "task": "save_currencies_rates_task",
        "schedule": crontab(hour=1, minute=5),
    }
}
