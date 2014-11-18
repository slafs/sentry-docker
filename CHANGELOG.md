# Changelog

## 2014-11-18

- added ``SENTRY_INTIAL_DOMAINS`` for allowed domains


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

