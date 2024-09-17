from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from datetime import timedelta


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')  # Replace 'your_project' with your project's name.

# Configure Celery using settings from Django settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load tasks from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# app.conf.CELERY_BEAT_SCHEDULE = {
#     'prune-presence': {
#         'task': 'channels_presence.tasks.prune_presences',
#         'schedule': timedelta(seconds=60)
#     },
#     'prune-rooms': {
#         'task': 'channels_presence.tasks.prune_rooms',
#         'schedule': timedelta(seconds=600)
#     }
