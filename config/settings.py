from .common import *

SECRET_KEY = config.get("DJANGO_SECRET")

DEBUG = bool(config.get("DEBUG"))

INTERNAL_IPS = [
    "127.0.0.1",
]
