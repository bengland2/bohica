#!/bin/bash

OK=0
NOTOK=1

timeout=30
poll_interval=5
ocos="oc -n openshift-storage"

which oc 2>/tmp/e || no_oc=1
which kubectl 2>/tmp/e2 || no_kubectl=1

if [ -n "$no_oc" ] ; then
   exit $NOTOK
fi
tool_pod=$($ocos get pod | awk '/rook-ceph-tool/{print $1}')
if [ -z $tool_pod ] ; then
   oc create -f toolbox.yaml
   for n in `seq 1 30` ; do
     sleep 1
     tool_pod=$($ocos get pod | awk '/rook-ceph-tool/{print $1}')
     if [ -n "$tool_pod" ] ; then
       break
     fi
   done
fi

wait_time=0
while [ $wait_time -lt $timeout ] ; do
    status=$(oc -n openshift-storage rsh $tool_pod ceph -s| grep HEALTH_OK)
    #status=$(kubectl -n rook-ceph exec -it $tool_pod bash -c ceph -s| grep HEALTH_OK)
    if [ -n "$status" ] ; then
        exit $OK
    fi
    sleep $poll_interval
    (( wait_time = $wait_time + $poll_interval ))
    echo "total wait time so far: $wait_time"
done
exit $NOTOK

