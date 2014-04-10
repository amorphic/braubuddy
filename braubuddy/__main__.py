"""
Braubuddy

TODO:
* auto-reload graphs every <interval> secs w/AJAX
* add cool/heat as background bar graph in light colours
* re-use graph function
* use units properly and everywhere
* add script start to setup.py
* replace RECENT_DATA output with a bus
* graphite output
"""

import sys
import logging
import cherrypy
import braubuddy
from cherrypy.process.plugins import Monitor

def main():
    '''
    Start the braubuddy engine and interface.
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
    # Initiate first engine cycle, otherwise no data available for <frequency> secs
    cherrypy.tree.apps['/engine'].root.cycle()
    cherrypy.engine.block()
    return 0

if __name__ == '__main__':
    sys.exit(main())
