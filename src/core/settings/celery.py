"""
Celery settings.
"""
from .redis import REDIS_URL


CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
