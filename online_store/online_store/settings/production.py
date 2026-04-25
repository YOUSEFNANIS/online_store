import os
import datetime
from .common import *


SECRET_KEY = os.environ['SECRET_KEY']
genai_key = os.environ['GENAI_KEY']

DEBUG = False

CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),
    'AUTH_COOKIE': 'access_token',  # Name of the cookie
    'AUTH_COOKIE_HTTP_ONLY': True,  # Prevents JS from reading the cookie
    'AUTH_COOKIE_SECURE': True,    # Set to True in production (HTTPS)
    'AUTH_COOKIE_SAMESITE': 'Lax',  # Prevents CSRF
}
