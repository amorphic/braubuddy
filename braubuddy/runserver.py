"""
Start Braubuddy
"""

import sys
import logging
import cherrypy
#TODO: clean these up
from cherrypy.process.plugins import Monitor
from cherrypy.lib import reprconf
import braubuddy

def main():
    """ 
    Start the braubuddy engine and interface.
    
    Involves some creative use of cherrypy's config loader to allow for a
    single user-editable config file.
    """

    braubuddy_config = reprconf.as_dict(braubuddy.CONFIG_FILE_BRAUBUDDY)
    cherrypy.config.update(braubuddy_config['global'])

    # Engine
    cherrypy.tree.mount(braubuddy.apps.Engine(), '/engine',
        config={'outputs': braubuddy_config['outputs']})
    # Dashboard
    cherrypy.tree.mount(
        braubuddy.apps.Dashboard(), '', config=braubuddy.CONFIG_FILE_DASHBOARD)
    # API
    cherrypy.tree.mount(
        braubuddy.apps.API(), '/api', config=braubuddy.CONFIG_FILE_API)

    # Add abbreviated units to global
    cherrypy.config['units_abbreviated'] = \
        braubuddy.thermometer.IThermometer.abbreviate_temp_units(
            cherrypy.config['thermostat'].get_units())

    # Append internal data storage to outputs
    engine_config = cherrypy.tree.apps['/engine'].config
    engine_config['outputs']['recent_data'] = braubuddy.RECENT_DATA

    # Job to regularly perform thermostat cycle
    cycle = Monitor(
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
