"""
Email settings.
"""
import os

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = bool(os.getenv("EMAIL_USE_TLS", False))

try:
    PASSWORD_RESET_TIMEOUT = int(os.getenv("PASSWORD_RESET_TIMEOUT"))        # type: ignore
except ValueError:
    PASSWORD_RESET_TIMEOUT = 14400
