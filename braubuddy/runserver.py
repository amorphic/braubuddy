"""
Start Braubuddy
"""

import sys
import logging
import cherrypy
import braubuddy
from cherrypy.process.plugins import Monitor


def main():
    """ 
    Start the braubuddy engine and interface.
    """
    # Mount applications
    cherrypy.config.update(braubuddy.CONFIG_FILE_BRAUBUDDY)

    # Engine
    cherrypy.tree.mount(
        braubuddy.apps.Engine(), '/engine', config=braubuddy.CONFIG_FILE_BRAUBUDDY)
    # Dashboard
    cherrypy.tree.mount(
        braubuddy.apps.Dashboard(), '', config=braubuddy.CONFIG_FILE_DASHBOARD)
    # API
    cherrypy.tree.mount(
        braubuddy.apps.API(), '/api', config=braubuddy.CONFIG_FILE_API)

    # Append internal data storage to outputs
    engine_config = cherrypy.tree.apps['/engine'].config
    engine_config['outputs']['recent_data'] = braubuddy.RECENT_DATA

    # Job to regularly perform thermostat cycle
    cycle = Monitor(
        cherrypy.engine,
        cherrypy.tree.apps['/engine'].root.cycle,
        frequency=engine_config['global']['frequency'],
        name='bb_engine')
    cycle.subscribe()

    # Start cherrypy engine
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()

    # Initiate first engine cycle to ensure data is available immediately
    cherrypy.tree.apps['/engine'].root.cycle()
    cherrypy.engine.block()
    return 0

if __name__ == '__main__':
    sys.exit(main())
