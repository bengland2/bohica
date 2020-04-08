#!/bin/bash

OK=0
NOTOK=1

status=$(ceph -f json -s > /tmp/status.json)
if [ $? != $OK ] ; then
    exit $NOTOK
fi

