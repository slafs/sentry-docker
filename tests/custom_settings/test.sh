#!/bin/bash

LAST_ERROR_CODE=0

nc -w 5 -vz sentryweb 9090
RET=$?
if [ "$RET" != "0" ]; then LAST_ERROR_CODE=$RET; fi

exit $LAST_ERROR_CODE
