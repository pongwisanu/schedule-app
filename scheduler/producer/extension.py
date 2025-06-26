from flask_apscheduler import APScheduler
from celery import Celery
from config import settings
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

scheduler = APScheduler()

celery = Celery()

celery.conf.broker_url = settings.BROKER_URL

mongo = MongoClient(
            settings.DSN,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
