import os
from .base import *
from corsheaders.defaults import default_headers
# import dj_database_url

DEBUG = True
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_HEADERS = list(default_headers) + ["ngrok-skip-browser-warning"]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
]


# # Using PRODUCTION DB for development
# DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':config 'athenas',
        'USER':config 'postgres',
        'PASSWORD': config'newpassword',
        'HOST':config 'localhost',
        'PORT':config '5432',
# Allow connections only from localhost
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

    }
}
