import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings.dev')

celery = Celery('messenger')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()