#!/usr/bin/env python3

import subprocess
import logging
import cherrypy
import atexit
import os
import sys

proc_fs_mountpoint = '/proc_sys_vm'

logging.basicConfig(filename='/tmp/dropcache.log', level=logging.DEBUG)
logger = logging.getLogger('dropcache')

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


# sanity check to make sure our k8s volume is actually
# hooked into the /proc filesystem

logger.info('debug log at /tmp/dropcache.log')
if not os.access('%s/dirty_ratio' % proc_fs_mountpoint, os.R_OK):
    logger.critical('No access to /proc filesystem, check volume')
    sys.exit(1)
if not os.access('%s/drop_caches' % proc_fs_mountpoint, os.W_OK):
    logger.critical('No write access to /proc filesystem, run as root')
    sys.exit(1)

svcPortNum=9435
portnumstr = os.getenv('KCACHE_DROP_PORT_NUM')
if portnumstr != None:
    svcPortNum = int(portnumstr)

def flush_log():
    logging.shutdown()

atexit.register(flush_log)

class DropKernelCache(object):

    @cherrypy.expose
    def index(self):
        return "Hi there\n"

    @cherrypy.expose
    def DropKernelCache(self):
        logger.info('asked for cache drop')
        os.sync()
        logger.info('completed sync call')
        with open('%s/drop_caches' % proc_fs_mountpoint, 'a') as dcf:
            dcf.write('3\n')
        logger.info('completed cache drop')
        return 'SUCCESS'

if __name__ == '__main__':
    config = { 
        'global': {
            'server.socket_host': '0.0.0.0' ,
            'server.socket_port': svcPortNum,
        },
    }
    cherrypy.config.update(config)
    cherrypy.quickstart(DropKernelCache())
