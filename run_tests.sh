#!/bin/bash

##
## this is a simple script to run series of tests
## and check if this project is doing OK.
##

#set -x

DIR_TO_TEST=${1:-"./tests"}
last_errorcode=0


for composefile in $(find $DIR_TO_TEST -name docker-compose.yml); do
    echo -e "\033[33m-------------------------\033[0m"
    echo -e "\033[33mtrying $composefile\033[0m"
    echo -e "\033[33m-------------------------\033[0m"

    COMPOSE="docker-compose -f $composefile"

    $COMPOSE build
    $COMPOSE run --rm test
    exitcode=$?
    if [ "$exitcode" == "0" ]; then
        echo -e "\033[32mSUCCESS $composefile\033[0m"
    else
        last_errorcode=$exitcode
        echo -e "\033[31mFAILURE $composefile\033[0m"
    fi

    $COMPOSE stop
    $COMPOSE rm -v --force
done

if [ "$last_errorcode" == "0" ]; then
    echo -e "\033[32mSUCCESS\033[0m"
else
    last_errorcode=$exitcode
    echo -e "\033[31mFAILURE\033[0m"
fi

exit $last_errorcode
