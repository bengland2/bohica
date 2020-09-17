#!/usr/bin/env python3
# Ceph OSD cache dropping service

import subprocess
import logging
import cherrypy
import atexit
import os
import sys

# process exit status
NOTOK = 1

logging_format = '%(asctime)-15s %(message)s'
logging.basicConfig(format=logging_format, level=logging.DEBUG)
logger = logging.getLogger('dropcache')


def flush_log():
    logging.shutdown()


atexit.register(flush_log)

# parse environment variables and log them

svcPortNum = 9435
portnumstr = os.getenv('CEPH_CACHE_DROP_PORT_NUM')
if portnumstr is not None:
    svcPortNum = int(portnumstr)
toolbox_pod_name = os.getenv('CEPH_TOOLBOX_POD_ID')
if toolbox_pod_name is None:
    logger.error('no CEPH_TOOLBOX_POD_ID env. var., shutting down')
    sys.exit(NOTOK)
toolbox_pod_namespace = os.getenv('CEPH_TOOLBOX_POD_NAMESPACE')
if toolbox_pod_namespace is None:
    toolbox_pod_namespace = 'openshift-storage'
logger.info('ceph cache drop port num %d, toolbox pod ID %s, namespace %s' %
            (svcPortNum, toolbox_pod_name, toolbox_pod_namespace))


class DropOSDCache(object):
    @cherrypy.expose
    def index(self):
        return "Hello from DropOSDCache\n"

    @cherrypy.expose
    def drop_osd_caches(self):
        result = subprocess.check_output(
                ['/opt/ceph_cache_drop/kubectl', '-n', toolbox_pod_namespace,
                 'exec', '-i', '-t', toolbox_pod_name, '--',
                 "/usr/bin/ceph", "tell", "osd.*", "cache", "drop"])
        logger.debug(result)
        return 'SUCCESS'


if __name__ == '__main__':
    logger.info('entering OSD cache drop service')

    config = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': svcPortNum,
        },
    }
    cherrypy.config.update(config)
    cherrypy.quickstart(DropOSDCache())
