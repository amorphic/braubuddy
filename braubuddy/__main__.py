"""
Braubuddy

TODO:
* replace RECENT_DATA output with a bus
* provide heavily commented config.example and tell users to copy it
* use units properly
* jinja2 template
 * css to make it pretty
 * graphs/graphics consuming api
* graphite output
"""

import os
import sys
import logging
import json
import cherrypy
import braubuddy
from datetime import datetime
from cherrypy.process.plugins import Monitor

# Temp/Controller data
## Get rid of this and use a queue or summat
RECENT_DATA = braubuddy.output.ListMemory()

def main():
    '''
    Start the braubuddy engine and interface
    '''

    # Load global config and mount applications
    cherrypy.config.update(braubuddy.CONFIG_BRAUBUDDY)
    cherrypy.tree.mount(braubuddy.apps.Engine(), '/engine', config=braubuddy.CONFIG_BRAUBUDDY)
    cherrypy.tree.mount(braubuddy.apps.Dashboard(), '', config=braubuddy.CONFIG_DASHBOARD)
    cherrypy.tree.mount(braubuddy.apps.API(), '/api', config=braubuddy.CONFIG_API)

    # Add recent data storage to outputs to be consumed by applications
    cherrypy.tree.apps['/engine'].config['outputs']['recent_data'] = braubuddy.RECENT_DATA

    # Create job to regularly perform thermostat cycle
    frequency = cherrypy.tree.apps['/engine'].config['components']['frequency']
    cycle = Monitor(cherrypy.engine, cherrypy.tree.apps['/engine'].root.cycle, frequency=frequency, name='bb_engine')
    cycle.subscribe()

    # Start cherrypy engine
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
    return 0

if __name__ == '__main__':
    sys.exit(main())
