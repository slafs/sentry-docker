# Contributing

If you feel like contributing to this repo or you think that something
is missing here please consider forking this repo and open a pull request.

## Guidelines

All files in this repo shouldn't be Docker specific
(besides ``Dockerfile`` of course :P).
That is you should be able to use a local installation of
sentry (after installing required system dependencies as stated in
``Dockerfile``) and use files in this repo as a starting point 
for your sentry installation (after tweaking some env var like for example
``SENTRY_DATA_DIR``)

## Tests

If you want to add a feature that requires some testing 
you can do this by creating a directory lets say ``feature_X``
inside ``tests/`` directory.

This directory has to contain at least one file called ``fig.yml``
which should define at least one service called ``test``.
This service should define a container which will run the check
whether or not your feature works with this image.
This could be any script like a simple netcat (nc) call to
check if a port is open on a given host.

To run the tests you have to install fig:

    pip install fig

Go to [fig.sh](http://www.fig.sh) for more info about how to install 
and use Fig.

``fig.yml`` has to be written as if it was run from the main directory
of this repo (the one that contains ``tests``, ``sentry_docker_conf.py`` etc.).
This is specially important when writing the ``build`` key.

Then you can run ``./run_tests.sh tests/feature_X``.

You can run all the tests by running ``run_tests.sh`` script
with no arguments.

Refer to ``tests/simple_services/`` for an example of a simple
testing script and a configuration file.

Unfortunately as for now you should provide some kind of
timeout (120 seconds should be enough) to let other containers
start properly (i.e. sentry could create the database tables etc.)

