"""
Braubuddy engine

TODO:
- layout
 - 'engine', 'cycle, 'api'?
  - each a separate class, separate config?
  - cycle config
   - not in braubuddy format?
   - separate from app config so not changed on update?
   - provide heavily commented config.example and tell users to copy it
- html template
- graphs/graphics consuming api
- graphite output
"""

import braubuddy 
import logging
import cherrypy
import sys
import json
from cherrypy.process.plugins import Monitor

# Temp/Controller data
RECENT_DATA = braubuddy.output.ListMemory()

# Config file
CONFIG = 'config/braubuddy'
CONFIG_APP = 'config/app'

class API(object):
    """
    Braubuddy API
    """

    @cherrypy.expose
    def index(self):
        # Return page w/API instructions
        return 'Braubuddy API'

    @cherrypy.expose
    def data(self):
        return unicode(RECENT_DATA.get_datapoints())

    @cherrypy.expose
    def set(self, temp):
        if temp:
            # Set engine temp to new temp (using queue?)
            pass
        return 'Set temp to {0}'.format(temp)

class Engine(object):
    """
    The Braubuddy Engine.
    """

    def __init__(self):

        self.api = API()

    @cherrypy.expose
    def index(self):
        # Serve html + js prettiness pointing at api
        return 'Braubuddy'

    def cycle(self):
        """
        Performs full thermostat cycle.
        """

        # Load Config
        e_conf = cherrypy.request.app.config['engine']
        envcontroller = e_conf['envcontroller']
        thermometer = e_conf['thermometer']
        thermostat = e_conf['thermostat']
        # Environment Input
        current_heat, current_cool = envcontroller.get_power_levels()
        current_temp = thermometer.get_temperature()
        required_heat, required_cool = thermostat.get_required_state(
            current_temp, current_heat, current_cool)
        # Set Power Levels
        envcontroller.set_heater_level(required_heat)
        envcontroller.set_cooler_level(required_cool)        
        # Output
        outputs = cherrypy.request.app.config['outputs']
        for name, output in outputs.iteritems():
            output.publish_status(current_temp, current_heat, current_cool)
        RECENT_DATA.publish_status(current_temp, current_heat, current_cool)

def main():

    # Create Braubuddy application
    braubuddy_engine = Engine()
    # Load Global config
    cherrypy.config.update(CONFIG)
    # Mount Braubuddy application
    cherrypy.tree.mount(braubuddy_engine, config=CONFIG)
    # Create job to regularly perform thermostat cycle
    cycle = Monitor(cherrypy.engine, braubuddy_engine.cycle,
        frequency=cherrypy.tree.apps[''].config['engine']['frequency'], 
        #frequency=cherrypy.config['engine']['frequency'], 
        name='bb_engine')
    cycle.subscribe()
    # Start cherrypy
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
    return 0

if __name__ == '__main__':
    sys.exit(main())
