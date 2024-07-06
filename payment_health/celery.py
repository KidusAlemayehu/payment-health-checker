from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payment_health.settings')

app = Celery('payment_health')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.enable_utc = False
app.autodiscover_tasks()