"""
Start Braubuddy

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
    cherrypy.tree.mount(
        braubuddy.apps.Engine(), '/engine', config=braubuddy.CONFIG_BRAUBUDDY)
    cherrypy.tree.mount(
        braubuddy.apps.Dashboard(), '', config=braubuddy.CONFIG_DASHBOARD)
    cherrypy.tree.mount(
        braubuddy.apps.API(), '/api', config=braubuddy.CONFIG_API)
    engine_config = cherrypy.tree.apps['/engine'].config

    # Add recent data storage to outputs to be consumed by applications
    engine_config['outputs']['recent_data'] = braubuddy.RECENT_DATA

    # Create job to regularly perform thermostat cycle
    frequency = engine_config['components']['frequency']
    cycle = Monitor(
        cherrypy.engine,
        cherrypy.tree.apps['/engine'].root.cycle,
        frequency=frequency,
        name='bb_engine')
    cycle.subscribe()

    # Start cherrypy engine
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()

    # Initiate first engine cycle, so graph data is available immediately
    cherrypy.tree.apps['/engine'].root.cycle()
    cherrypy.engine.block()
    return 0

if __name__ == '__main__':
    sys.exit(main())
