#!/usr/bin/env python

import subprocess
import logging
import cherrypy

stdout_log = open('/tmp/wait-for-healthy.log', 'w')

logger = logging.getLogger('wait_healthy')

class WaitForHealthy(object):
    @cherrypy.expose
    def index(self):
        try:
            result = subprocess.check_output(
                ["/bin/sh", "wait-for-ceph-healthy.sh"])
        except subprocess.CalledProcessError as e:
            logger.error('ceph cluster did not get healthy')
            logger.exception(e)
            return 'FAIL'
        logger.info(result)
        return 'SUCCESS'

if __name__ == '__main__':
    config = { 
        'global': {
            'server.socket_host': '0.0.0.0' ,
            'server.socket_port': 9434,
        },
    }
    cherrypy.config.update(config)
    cherrypy.quickstart(WaitForHealthy())
