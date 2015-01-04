#!/bin/bash

HAS_ERRORS=0
TIMEOUT=210  # seconds

declare -A services
services[redis]=6379
services[postgresdb]=5432
services[sentryweb]=9000

echo
echo "waiting for services"

trap "exit" INT
for service in ${!services[@]}; do  # loop through all services

    port=${services[${service}]}

    echo "trying $service:$port"
    for i in $(seq 1 $TIMEOUT); do

        nc -w 5 -z $service $port 2>&1
        RET_CODE=$?
        if [ "$RET_CODE" -ne "0" ]; then
            echo -n "."
            sleep 1
        else
            echo "$service:$port OK"
            break
        fi

    done

    # after a timeout (or break) check if there still were errors
    if [ "$RET_CODE" -ne "0" ]; then
        HAS_ERRORS=$RET_CODE
    fi

done

exit $HAS_ERRORS
