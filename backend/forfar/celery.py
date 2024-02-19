import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forfar.settings')

app = Celery('forfar')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
