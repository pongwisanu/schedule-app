from flask_apscheduler import APScheduler
from celery import Celery
from config import settings

scheduler = APScheduler()

celery = Celery()

celery.conf.broker_url = settings.BROKER_URL