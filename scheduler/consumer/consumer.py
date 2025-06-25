from celery import Celery
from config import settings

celery = Celery()
celery.conf.broker_url = settings.BROKER_URL

import job.first_trigger

# How to start 
# celery -A consumer worker --loglevel=info