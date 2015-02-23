# Changelog

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

