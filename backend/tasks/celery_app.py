"""
Celery configuration and initialization
"""
import os
from celery import Celery
from app.config import settings

# Initialize Celery app
celery_app = Celery(
    "data_analyst_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["tasks.upload_tasks", "tasks.report_tasks", "tasks.ml_tasks"],
)

# Load config from settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max
)
