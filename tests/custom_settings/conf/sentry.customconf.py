# This file is just Python, with a touch of Django which means you
# you can inherit and tweak settings to your hearts content.
from sentry.conf.server import *  # noqa
import os.path

from decouple import config
import dj_database_url
import django_cache_url

CONF_ROOT = os.path.dirname(__file__)
DATA_DIR = config('SENTRY_DATA_DIR', default='/data')
DEFAULT_SQLITE_DB_PATH = os.path.join(DATA_DIR, 'sentry.db')

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///{0}'.format(DEFAULT_SQLITE_DB_PATH))
}

CACHES = {'default': django_cache_url.config() }

SENTRY_URL_PREFIX = config('SENTRY_URL_PREFIX')  # No trailing slash!

SENTRY_WEB_HOST = config('SENTRY_WEB_HOST', default='0.0.0.0')
SENTRY_WEB_PORT = config('SENTRY_WEB_PORT', default=9090, cast=int)
SECRET_KEY = config('SECRET_KEY')
