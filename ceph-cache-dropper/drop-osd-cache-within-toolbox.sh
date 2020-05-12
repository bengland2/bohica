#!/bin/bash

OK=0
NOTOK=1


osds=$(ceph osd tree | awk '/osd\./{print $4}')
if [ $? != $OK ] ; then
    exit $NOTOK
fi

for o in $osds ; do
    cmd="ceph tell $o cache drop"
    echo $cmd
    eval "$cmd &"
    pids="$pids $!"
done
s=$OK
for p in $pids ; do 
    wait $p || s=$?
done
exit $s
