from __future__ import absolute_import , unicode_literals
import os
from django.urls.conf import include
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','busbook.settings')
BASE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
app = Celery('busbook')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_url = BASE_REDIS_URL
