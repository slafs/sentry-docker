# Changelog

## 2016-03-07

- Upgraded to Sentry ``8.0``

## 2015-12-18

- added `CELERY_RESULT_SERIALIZER`, `CELERY_TASK_SERIALIZER`
  and `CELERY_ACCEPT_CONTENT` configs to avoid `C_FORCE_ROOT` env var
  (default values support `pickle` for backwards compatibility).

## 2015-11-16

- updated ``Sentry`` to 7.7.4
- merged forgotten changes to dev

## 2015-11-11

- updated ``Sentry`` to 7.7.1
- updated ``django-auth-ldap`` to 1.2.7
- updated ``django-redis`` to 4.3.0
- updated ``python-decouple`` to 3.0
- fixed building dev version (8.0.0.dev0) (credit goes to: @yurtaev)
- creating superuser via python script

## 2015-08-29

- updated ``Sentry`` to 7.7.0 and dropped ``django-json`` fix

## 2015-08-26

- updated ``Sentry`` to 7.6.2

## 2015-08-24

- add `.dockerignore` file
- updated ``django-cache-url`` to 1.0.0 (watch out for trailing `/`)
- updated ``django-redis`` to 4.2.0

## 2015-08-20

- Added `nestedGroupOfNames` `LDAP_GROUP_TYPE`
- Make use of `LDAP_GROUP_STAFF`

## 2015-08-19

- fix migration issue (https://github.com/getsentry/sentry/issues/1648)
- allow for a simple database accessibility check (via ``SENTRY_DOCKER_DO_DB_CHECK`` env var)
- updated ``Sentry`` to 7.5.6

## 2015-06-25

- remove ``nydus`` as an explicit requirement (see #28)

## 2015-06-22

- updated ``Sentry`` to 7.5.4

## 2015-06-08

- revert django-redis to 3.8.4 due to #26

## 2015-05-20

- updated ``requirements.txt`` (``django-redis``, ``hiredis`` and ``django-auth-ldap`` )
- added support for posixGroup in LDAP auth backend (credit goes to: @grundleborg)

## 2015-03-26

- updated ``Sentry`` to 7.4.3

## 2015-03-17

- Add support for REMOTE_USER authentication (credit goes to: @abesto)

## 2015-03-16

- Add support for SENTRY_PUBLIC (credit goes to: @abesto)

## 2015-03-12

- Add support for configuring time-series storage (credit goes to:
  @abesto)

## 2015-03-07

- Properly pass SIGTERM to sentry process (credit goes to: @lorenz)
- new Sentry 7.4.X
- move from fig to docker-compose while testing
- when ``SENTRY_USE_REDIS_BUFFERS`` is used then ``sentry.cache.redis.RedisCache`` is configured as a ``SENTRY_CACHE``

## 2015-02-23

- updated ``requirements.txt`` (``django-redis``)
- new Sentry 7.3.X

## 2015-02-12

- updated ``requirements.txt`` (``django-auth-ldap`` and ``hiredis``)
- new Sentry 7.2.X

## 2015-01-27

- new tag/branch ``7.1``
- updated ``requirements.txt`` (``django-redis``)

## 2015-01-08

- updated ``requirements.txt`` (``django-redis``)

## 2015-01-04

- updated ``requirements.txt`` (``django-auth-ldap``)
- new Sentry 7.0.X and several new build tags on docker hub

## 2014-12-07

- updated ``django-redis`` to 3.8.0
- provide builds from sentry's master github branch

## 2014-12-01

- added ``SENTRY_ALLOW_ORIGIN`` - thanks to @josh-devops-center

## 2014-11-30

- FIX: determine platform when creating a project (via ``SENTRY_INITIAL_PLATFORM``) - thanks to @josh-devops-center

## 2014-11-20

- added ``SENTRY_INTIAL_DOMAINS`` for allowed domains (see #7)
- allow setting ``SENTRY_SECURE_PROXY_SSL_HEADER`` and ``SENTRY_USE_X_FORWARDED_HOST`` (see #6)

## 2014-11-05

- update django-redis requirement
- add some cleanup at the end of build process
- add new env vars for initial team, project and project key (``SENTRY_INITIAL_*``)
- add new command ``prepare`` for the wrapper script to just prepare the datbase
  and other stuff without running the http sevice.

## 2014-10-09

- change the name of the config script (this is a possible *breaking change*
  but now you can easily extend this image and configuration)
- make it possible to "test" this image

## 2014-10-06

- updated ``requirements.txt`` (``django-auth-ldap`` and ``hiredis``)
- added some contribution guidelines

## 2014-09-09

- added new setting ``SENTRY_ALLOW_REGISTRATION`` (credit goes to: @lukas-hetzenecker)
- added LDAP backend support (``SENTRY_USE_LDAP`` and ``LDAP_*`` settings)
  (credit goes to: @lukas-hetzenecker)

