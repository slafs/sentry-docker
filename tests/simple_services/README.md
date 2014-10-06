Simple tests
=============

This directory contains a simple script that tests
if all linked containers are accessible on the given ports.

The script is run inside a container (described by a
``Dockerfile`` in this directory).

The ``fig.yml`` in this directory is written as if 
it was run from the main directory of this repo.
It must have a service named ``test``.

Go to [fig.sh](http://www.fig.sh) for more info about Fig.
