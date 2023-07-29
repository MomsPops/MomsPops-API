"""
Database settings.
"""
import os
from socket import gethostbyname


if os.getenv("DOCKER"):
    DATABASES = {
        "default": {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv("DB_NAME"),
            "HOST": gethostbyname(os.getenv("DB_HOST")),
            "PORT": os.getenv("DB_PORT"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD")
        }
    }
else:
    DATABASES = {
        "default": {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': "momspops.sqlite3"
        }
    }
