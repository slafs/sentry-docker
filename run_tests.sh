#!/bin/bash

##
## this is a simple script to run series of tests
## and check if this project is doing OK.
##

#set -x

DIR_TO_TEST=${1:-"./tests"}
last_errorcode=0


for figfile in $(find $DIR_TO_TEST -name fig.yml); do
    echo -e "\033[33m-------------------------\033[0m"
    echo -e "\033[33mtrying $figfile\033[0m"
    echo -e "\033[33m-------------------------\033[0m"

    FIG="fig -f $figfile"

    $FIG build
    $FIG run --rm test
    exitcode=$?
    if [ "$exitcode" == "0" ]; then
        echo -e "\033[32mSUCCESS $figfile\033[0m"
    else
        last_errorcode=$exitcode
        echo -e "\033[31mFAILURE $figfile\033[0m"
    fi

    $FIG stop
    $FIG rm -v --force
done

if [ "$last_errorcode" == "0" ]; then
    echo -e "\033[32mSUCCESS\033[0m"
else
    last_errorcode=$exitcode
    echo -e "\033[31mFAILURE\033[0m"
fi

exit $last_errorcode
