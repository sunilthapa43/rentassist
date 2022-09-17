#post_save(payment):
# run scheduled task at day 29, 30 and day 31 to create notification

import os

from celery import Celery, shared_task
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rentassist.settings')

app = Celery('rentassist')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'execute_daily': {
            'task': 'rentapp.tasks.check_deadline',
            'schedule': crontab(hour=0, minute=0),
            'args': (16, 16),
        },
    'execute_daily_a': {
            'task': 'rentapp.tasks.agreement_status',
            'schedule': crontab(hour=0, minute=0),
            'args': (16, 16),
        },
    }

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.timezone = 'UTC'



