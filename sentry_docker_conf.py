# This file is just Python, with a touch of Django which means you
# you can inherit and tweak settings to your hearts content.
from sentry.conf.server import *  # noqa
import os.path

from decouple import config
import dj_database_url
import django_cache_url
import functools

CONF_ROOT = os.path.dirname(__file__)
DATA_DIR = config('SENTRY_DATA_DIR', default='/data')
DEFAULT_SQLITE_DB_PATH = os.path.join(DATA_DIR, 'sentry.db')

REDIS_HOST = config('SENTRY_REDIS_HOST', default='redis')
REDIS_PORT = config('SENTRY_REDIS_PORT', default=6379, cast=int)

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///{0}'.format(DEFAULT_SQLITE_DB_PATH))
}

if 'postgres' in DATABASES['default']['ENGINE']:
    DATABASES['default']['ENGINE'] = 'sentry.db.postgres'

# You should not change this setting after your database has been created
# unless you have altered all schemas first
SENTRY_USE_BIG_INTS = config('SENTRY_USE_BIG_INTS', default=False, cast=bool)

SENTRY_SINGLE_ORGANIZATION = config('SENTRY_SINGLE_ORGANIZATION', default=True, cast=bool)

CACHES = {'default': django_cache_url.config() }
SENTRY_CACHE = 'sentry.cache.django.DjangoCache'

SENTRY_PUBLIC = config('SENTRY_PUBLIC', default=False, cast=bool)

def nydus_config(from_env_var):
    """
    Generate a Nydus Redis configuration from an ENV variable of the form "server:port,server:port..."
    Default to REDIS_HOST:REDIS_PORT if the ENV variable is not provided.
    """
    redis_servers_cast = lambda x: list(r.split(':') for r in x.split(','))
    servers = config(from_env_var, default='{0}:{1}'.format(REDIS_HOST, REDIS_PORT), cast=redis_servers_cast)
    _redis_hosts = {}

    for r_index, r_host_pair in enumerate(servers):
        _redis_hosts[r_index] = {'host': r_host_pair[0], 'port': int(r_host_pair[1])}

    return {
        'hosts': _redis_hosts
    }


############################
# General Sentry options ##
############################
SENTRY_OPTIONS = {
    # You MUST configure the absolute URI root for Sentry:
    'system.url-prefix': config('SENTRY_URL_PREFIX'),
    'system.admin-email': config('SENTRY_ADMIN_EMAIL', default='root@localhost'),
}

###########
# Queue ##
###########

# See http://sentry.readthedocs.org/en/latest/queue/index.html for more
# information on configuring your queue broker and workers. Sentry relies
# on a Python framework called Celery to manage queues.

# You can enable queueing of jobs by turning off the always eager setting:
CELERY_ALWAYS_EAGER = config('CELERY_ALWAYS_EAGER', default=True, cast=bool)
DEFAULT_BROKER_URL = 'redis://{0}:{1}/1'.format(REDIS_HOST, REDIS_PORT)

BROKER_URL = config('SENTRY_BROKER_URL', default=DEFAULT_BROKER_URL)

CELERY_RESULT_SERIALIZER = config('CELERY_RESULT_SERIALIZER', default='pickle')
CELERY_TASK_SERIALIZER = config('CELERY_TASK_SERIALIZER', default='pickle')
CELERY_ACCEPT_CONTENT = config('CELERY_ACCEPT_CONTENT', default='pickle,json', cast=lambda x: x.split(','))

####################
# Update Buffers ##
####################

# Buffers (combined with queueing) act as an intermediate layer between the
# database and the storage API. They will greatly improve efficiency on large
# numbers of the same events being sent to the API in a short amount of time.
# (read: if you send any kind of real data to Sentry, you should enable buffers)

# You'll need to install the required dependencies for Redis buffers:
#   pip install redis hiredis nydus
#

SENTRY_USE_REDIS_BUFFERS = config('SENTRY_USE_REDIS_BUFFERS', default=False, cast=bool)

if SENTRY_USE_REDIS_BUFFERS:
    SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
    SENTRY_REDIS_OPTIONS = nydus_config('SENTRY_REDIS_BUFFERS')
    SENTRY_CACHE = 'sentry.cache.redis.RedisCache'

#######################
# Time-series Storage #
#######################
# Sentry provides a service to store time-series data. Primarily this
# is used to display aggregate information for events and projects, as
# well as calculating (in real-time) the rates of events.

SENTRY_USE_REDIS_TSDB = config('SENTRY_USE_REDIS_TSDB', default=False, cast=bool)

if SENTRY_USE_REDIS_TSDB:
    SENTRY_TSDB = 'sentry.tsdb.redis.RedisTSDB'
    SENTRY_TSDB_OPTIONS = nydus_config('SENTRY_REDIS_TSDBS')

################
# Web Server ##
################

# If you're using a reverse proxy, you should enable the X-Forwarded-Proto
# and X-Forwarded-Host headers, and uncomment the following settings
SECURE_PROXY_SSL_HEADER = config('SENTRY_SECURE_PROXY_SSL_HEADER', default=None, cast=lambda x: tuple(x.split(',')) if x else None)
USE_X_FORWARDED_HOST = config('SENTRY_USE_X_FORWARDED_HOST', default=False, cast=bool)

SENTRY_WEB_HOST = config('SENTRY_WEB_HOST', default='0.0.0.0')
SENTRY_WEB_PORT = config('SENTRY_WEB_PORT', default=9000, cast=int)
SENTRY_WEB_OPTIONS = {
    'workers': config('SENTRY_WORKERS', default=3, cast=int),  # the number of sentry web workers
    'limit_request_line': 0,  # required for raven-js
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
    'errorlog' : os.path.join(DATA_DIR, 'sentry_web_error.log'),
    'accesslog' : os.path.join(DATA_DIR, 'sentry_web_access.log'),
}

# allows JavaScript clients to submit cross-domain error reports. Useful for local development
SENTRY_ALLOW_ORIGIN = config('SENTRY_ALLOW_ORIGIN', default=None)

#################
# Mail Server ##
#################

# For more information check Django's documentation:
#  https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#e-mail-backends

EMAIL_BACKEND = config('SENTRY_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

EMAIL_HOST = config('SENTRY_EMAIL_HOST', default='localhost')
EMAIL_HOST_PASSWORD = config('SENTRY_EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('SENTRY_EMAIL_HOST_USER', default='')
EMAIL_PORT = config('SENTRY_EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('SENTRY_EMAIL_USE_TLS', default=False, cast=bool)

# The email address to send on behalf of
SERVER_EMAIL = config('SENTRY_SERVER_EMAIL', default='root@localhost')

###########
# etc. ##
###########

SENTRY_FEATURES['auth:register'] = config('SENTRY_ALLOW_REGISTRATION', default=False, cast=bool)

# If this file ever becomes compromised, it's important to regenerate your SECRET_KEY
# Changing this value will result in all current sessions being invalidated
SECRET_KEY = config('SECRET_KEY')

# http://twitter.com/apps/new
# It's important that input a callback URL, even if its useless. We have no idea why, consult Twitter.
TWITTER_CONSUMER_KEY = config('TWITTER_CONSUMER_KEY', default='')
TWITTER_CONSUMER_SECRET = config('TWITTER_CONSUMER_SECRET', default='')

# http://developers.facebook.com/setup/
FACEBOOK_APP_ID = config('FACEBOOK_APP_ID', default='')
FACEBOOK_API_SECRET = config('FACEBOOK_API_SECRET', default='')

# http://code.google.com/apis/accounts/docs/OAuth2.html#Registering
GOOGLE_OAUTH2_CLIENT_ID = config('GOOGLE_OAUTH2_CLIENT_ID', default='')
GOOGLE_OAUTH2_CLIENT_SECRET = config('GOOGLE_OAUTH2_CLIENT_SECRET', default='')

# https://github.com/settings/applications/new
GITHUB_APP_ID = config('GITHUB_APP_ID', default='')
GITHUB_API_SECRET = config('GITHUB_API_SECRET', default='')

# https://trello.com/1/appKey/generate
TRELLO_API_KEY = config('TRELLO_API_KEY', default='')
TRELLO_API_SECRET = config('TRELLO_API_SECRET', default='')

# https://confluence.atlassian.com/display/BITBUCKET/OAuth+Consumers
BITBUCKET_CONSUMER_KEY = config('BITBUCKET_CONSUMER_KEY', default='')
BITBUCKET_CONSUMER_SECRET = config('BITBUCKET_CONSUMER_SECRET', default='')

# custom settings
ALLOWED_HOSTS = ['*']
LOGGING['disable_existing_loggers'] = False

SENTRY_BEACON = config('SENTRY_BEACON', default=True, cast=bool)

####################
# LDAP settings ##
####################

SENTRY_USE_LDAP = config('SENTRY_USE_LDAP', default=False, cast=bool)

if SENTRY_USE_LDAP:
    import ldap
    from django_auth_ldap.config import LDAPSearch, GroupOfUniqueNamesType, PosixGroupType, NestedGroupOfNamesType

    AUTH_LDAP_SERVER_URI = config('LDAP_SERVER', default='ldap://localhost')

    AUTH_LDAP_BIND_DN = config('LDAP_BIND_DN', default='')
    AUTH_LDAP_BIND_PASSWORD = config('LDAP_BIND_PASSWORD', default='')

    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        config('LDAP_USER_DN'),
        ldap.SCOPE_SUBTREE,
        config('LDAP_USER_FILTER', default='(&(objectClass=inetOrgPerson)(cn=%(user)s))')
    )

    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        config('LDAP_GROUP_DN', default=''),
        ldap.SCOPE_SUBTREE,
        config('LDAP_GROUP_FILTER', default='(objectClass=groupOfUniqueNames)')
    )

    if config('LDAP_GROUP_TYPE', default='') == 'groupOfUniqueNames':
        AUTH_LDAP_GROUP_TYPE = GroupOfUniqueNamesType()
    elif config('LDAP_GROUP_TYPE', default='') == 'posixGroup':
        AUTH_LDAP_GROUP_TYPE = PosixGroupType()
    elif config('LDAP_GROUP_TYPE', default='') == 'nestedGroupOfNames':
        AUTH_LDAP_GROUP_TYPE = NestedGroupOfNamesType()

    AUTH_LDAP_REQUIRE_GROUP = config('LDAP_REQUIRE_GROUP', default=None)
    AUTH_LDAP_DENY_GROUP = config('LDAP_DENY_GROUP', default=None)

    AUTH_LDAP_USER_ATTR_MAP = {
        'first_name': config('LDAP_MAP_FIRST_NAME', default='givenName'),
        'last_name': config('LDAP_MAP_LAST_NAME', default='sn'),
        'email': config('LDAP_MAP_MAIL', default='mail')
    }

    ldap_is_active    = config('LDAP_GROUP_ACTIVE', default='')
    ldap_is_superuser = config('LDAP_GROUP_SUPERUSER', default='')
    ldap_is_staff     = config('LDAP_GROUP_STAFF', default='')

    if ldap_is_active or ldap_is_superuser or ldap_is_staff:
        AUTH_LDAP_USER_FLAGS_BY_GROUP = {
            'is_active': ldap_is_active,
            'is_superuser': ldap_is_superuser,
            'is_staff': ldap_is_staff,
        }

    AUTH_LDAP_FIND_GROUP_PERMS = config('LDAP_FIND_GROUP_PERMS', default=False, cast=bool)

    # Cache group memberships for an hour to minimize LDAP traffic
    AUTH_LDAP_CACHE_GROUPS = config('LDAP_CACHE_GROUPS', default=True, cast=bool)
    AUTH_LDAP_GROUP_CACHE_TIMEOUT = config('LDAP_GROUP_CACHE_TIMEOUT', default=3600, cast=int)

    AUTHENTICATION_BACKENDS = AUTHENTICATION_BACKENDS + (
        'django_auth_ldap.backend.LDAPBackend',
    )

    # setup logging for django_auth_ldap
    import logging
    logger = logging.getLogger('django_auth_ldap')
    logger.addHandler(logging.StreamHandler())
    ldap_loglevel = getattr(logging, config('LDAP_LOGLEVEL', default='DEBUG'))
    logger.setLevel(ldap_loglevel)

##############################
# REMOTE_USER authentication #
##############################

SENTRY_USE_REMOTE_USER = config('SENTRY_USE_REMOTE_USER', default=False, cast=bool)

if SENTRY_USE_REMOTE_USER:
    AUTHENTICATION_BACKENDS += ('django.contrib.auth.backends.RemoteUserBackend',)

    AUTH_REMOTE_USER_HEADER = config('AUTH_REMOTE_USER_HEADER', default=None)
    if AUTH_REMOTE_USER_HEADER:
        # The lazy hack is required because importing RemoteUserMiddleware at load time leads to a circular import
        # The name is upper camel case because that's the only way to expose values from this config file
        def build_LAZY_CUSTOM_REMOTE_USER_MIDDLEWARE(header, *args, **kwargs):
            from django.contrib.auth.middleware import RemoteUserMiddleware
            class CustomRemoteUserMiddleware(RemoteUserMiddleware):
               pass
            CustomRemoteUserMiddleware.header = header
            return CustomRemoteUserMiddleware(*args, **kwargs)
        LAZY_CUSTOM_REMOTE_USER_MIDDLEWARE = functools.partial(build_LAZY_CUSTOM_REMOTE_USER_MIDDLEWARE, AUTH_REMOTE_USER_HEADER)
        MIDDLEWARE_CLASSES += ('sentry_config.LAZY_CUSTOM_REMOTE_USER_MIDDLEWARE',)
    else:
        MIDDLEWARE_CLASSES += ('django.contrib.auth.middleware.RemoteUserMiddleware',)
