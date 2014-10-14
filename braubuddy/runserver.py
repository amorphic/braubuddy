"""
Start Braubuddy
"""

import sys
import cherrypy
import braubuddy


def main():
    """
    Start the braubuddy engine and interface.

    Involves some creative use of cherrypy's config loader to allow for a
    single user-editable config file.
    """

    # First load everything fron the config file into a dict. 
    try:
        braubuddy_config = cherrypy.lib.reprconf.as_dict(
            braubuddy.CONFIG_FILE_BRAUBUDDY)
    except Exception as err:
        print err
        return -1
    
    # Now initialise the various parts of the application with the relevant
    # pieces of config.

    # Global
    cherrypy.config.update(braubuddy_config['global'])
    # Engine
    engine_config = {'outputs': braubuddy_config['outputs']}
    cherrypy.tree.mount(
        braubuddy.apps.Engine(), '/engine', config=engine_config)
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
    cycle = cherrypy.process.plugins.Monitor(
        cherrypy.engine,
        cherrypy.tree.apps['/engine'].root.cycle,
        frequency=cherrypy.config['frequency'],
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
