#!/bin/bash

LAST_ERROR_CODE=0

nc -w 5 -vz redis 6379
RET=$?
if [ "$RET" != "0" ]; then LAST_ERROR_CODE=$RET; fi

nc -w 5 -vz postgresdb 5432
RET=$?
if [ "$RET" != "0" ]; then LAST_ERROR_CODE=$RET; fi

nc -w 5 -vz sentryweb 9000
RET=$?
if [ "$RET" != "0" ]; then LAST_ERROR_CODE=$RET; fi

exit $LAST_ERROR_CODE
