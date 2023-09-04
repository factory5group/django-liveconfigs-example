# quick_publisher/celery.py

import os

from celery import Celery
from celery.signals import setup_logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'liveconfigs_example.settings')

app = Celery('simpleapp')
app.config_from_object('liveconfigs_example.settings', namespace="CELERY")


@setup_logging.connect
def config_loggers(*args, **kwags):
    from logging.config import dictConfig

    from django.conf import settings
    dictConfig(settings.LOGGING)


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {

}
