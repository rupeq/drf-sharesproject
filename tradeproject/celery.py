from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tradeproject.settings')

app = Celery('tradeproject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_shedule = {
    "get_trade": {
        "task": "tradeapi.worker.get_trade",
        "schedule": 60,
    }
}