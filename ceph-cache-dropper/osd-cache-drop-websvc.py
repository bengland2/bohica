#!/usr/bin/env python

# Ceph OSD cache dropping service
# must run as privileged pod, but pods that call it
# do not have to, and more than one workload can make use of it
# to use it:
# # oc create -f dropper.yml
# # drop_pod_ip=$(oc -n openshift-storage get pod -o wide | awk '/drop/{print $1}')
# # curl http://$drop_pid_ip:9432/drop_osd_caches
# SUCCESS

import subprocess
import logging
import cherrypy
import atexit
import os
import sys

#logging.basicConfig(filename='/tmp/dropcache.log', level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('dropcache')
logger.setLevel(logging.DEBUG)

def flush_log():
    logging.shutdown()

atexit.register(flush_log)

class DropOSDCache(object):
    @cherrypy.expose
    def index(self):
        return "Hello from DropOSDCache\n"

    @cherrypy.expose
    def drop_osd_caches(self):
        try:
            result = subprocess.check_output(
                ["/usr/bin/ceph", "tell", "osd.*", "cache", "drop"])
            logger.debug(result)
        except subprocess.CalledProcessError as e:
            logger.error('failed to drop cache')
            logger.exception(e)
            return 'FAIL'
        return 'SUCCESS'

if __name__ == '__main__':
    try:
        result = subprocess.Popen(
            ["/bin/sh", "-c", "/usr/local/bin/toolbox.sh"])
    except subprocess.CalledProcessError as e:
        logger.error('failed to source toolbox')
        logger.exception(e)
        sys.exit(3)
    if not os.path.exists('/etc/ceph/ceph.conf'):
        logger.error('DID NOT FIND ceph.conf')
        sys.exit(2)
    logger.info('entering service')

    config = { 
        'global': {
            'server.socket_host': '0.0.0.0' ,
            'server.socket_port': 9432,
        },
    }
    cherrypy.config.update(config)
    cherrypy.quickstart(DropOSDCache())
