from .base import *

ALLOWED_HOSTS = ["*"]
CORS_ALLOWED_ORIGINS = ["https://athenas-production.up.railway.app", "https://athenas-frontend.vercel.app", "https://ehs.dcubix.com", "http://localhost:3000",]
CSRF_TRUSTED_ORIGINS = ["https://athenas-production.up.railway.app", "https://athenas-frontend.vercel.app", "https://ehs.dcubix.com", "http://localhost:3000",]