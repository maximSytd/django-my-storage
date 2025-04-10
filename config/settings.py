import decouple

from .common import *


SECRET_KEY = config.get("DJANGO_SECRET")

DEBUG = bool(config.get("DEBUG"))

INTERNAL_IPS = ["127.0.0.1"]

APP_LABEL = "My storage"

redis_host = decouple.config("REDIS_HOST")
redis_port = decouple.config("REDIS_PORT", cast=int)
redis_db = decouple.config("REDIS_DB", cast=int)

CELERY_TASK_DEFAULT_QUEUE = (
    f"{APP_LABEL.lower().replace(' ', '-')}"
)
CELERY_BROKER_URL = f"redis://{redis_host}:{redis_port}/{redis_db}"
CELERY_RESULT_BACKEND = f"redis://{redis_host}:{redis_port}/{redis_db}"

# Setting needed for redis health check
REDIS_URL = f"redis://{redis_host}:{redis_port}/{redis_db}"

CACHES["default"].update(
    LOCATION=REDIS_URL,
)
