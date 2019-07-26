#!/usr/bin/env bash
if [ -e $1 ]; then
    docker ps --no-trunc | grep -F -f $1 && echo doing && exit 1
    echo finish
    exit 0
fi
echo $1 not file
exit -1
