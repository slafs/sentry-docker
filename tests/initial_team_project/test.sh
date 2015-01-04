#!/bin/bash


HAS_ERRORS=0
TIMEOUT=210  # seconds

echo
echo "waiting for sentryweb:9000"

trap "exit" INT
for i in $(seq 1 $TIMEOUT); do
    nc -w 5 -z sentryweb 9000
    RET=$?
    HAS_ERRORS=$RET
    if [ "$RET" != "0" ]; then
        echo -n "."
        sleep 1
    else
        echo "sentryweb:9000 OK"
        sleep 2
        raven test
        HAS_ERRORS=$?
        break
    fi
done

exit $HAS_ERRORS
