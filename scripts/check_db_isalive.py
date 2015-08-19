#!/usr/bin/env python
# encoding: utf-8
"""
Simple script to determine if the database is already running
"""
from __future__ import print_function
import sys
import time

# Bootstrap the Sentry environment
from sentry.utils.runner import configure
configure()

# Do something crazy
from django.db import connections, OperationalError


def is_db_alive(conn):
    try:
        c = conn.cursor()  # this will take some time if error
    except OperationalError:
        reachable = False
    else:
        reachable = True
        c.close()

    return reachable


def main():
    max_retries = 10
    sleep_time = 3

    if len(sys.argv) > 1:
        max_retries = int(sys.argv[1])

    if len(sys.argv) > 2:
        sleep_time = int(sys.argv[2])

    conn = connections['default']

    for i in range(max_retries):

        if is_db_alive(conn):
            sys.exit(0)

        time.sleep(sleep_time)

    sys.exit(1)


if __name__ == '__main__':
    main()
