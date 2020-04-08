#!/usr/bin/env python

import subprocess
import logging
import cherrypy
import json

timeout = 3600
poll_rate = 5.

stdout_log = open('/tmp/wait-for-healthy.log', 'w')

logger = logging.getLogger('wait_healthy')

class WaitForHealthy(object):
    @cherrypy.expose
    def index(self):
        wait_time = 0.
        while wait_time < timeout:
            try:
                result = subprocess.check_output(
                    ["ceph", "-f", "json", "status"])
                s = json.loads(result)
                overall = s['health']['status'] 
                if overall == 'HEALTH_OK':
                    break
                logger.warn('health status %s' % overall)
            except subprocess.CalledProcessError as e:
                logger.error('could not get ceph status')
                logger.exception(e)
                return 'FAIL'
            if result != '':
                logger.info(json.dumps(result['health']))
            time.sleep(poll-rate)
            wait_time += poll_rate
            logger.info('waited %f sec' % wait_time)
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
