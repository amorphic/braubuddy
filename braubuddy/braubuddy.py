"""
Braubuddy

TODO:
- code layout
 - outputs need a better home
 - provide heavily commented config.example and tell users to copy it
- html template
 - basic template
 - graphs/graphics consuming api
- graphite output
"""
import logging
import cherrypy
import os
import sys
import json
import thermostat
import thermometer
import envcontroller
import output
import engine
from cherrypy.process.plugins import Monitor

# Temp/Controller data
RECENT_DATA = output.ListMemory()

# Config file
THIS_DIR = os.path.dirname(__file__)
CONFIG_BRAUBUDDY = os.path.join(THIS_DIR, 'config/braubuddy')
CONFIG_API = os.path.join(THIS_DIR, 'config/api')

class API(object):
    """
    Braubuddy API
    """

    @cherrypy.expose
    def index(self):
        '''
        Return page w/API instructions
        '''
        return 'Braubuddy API'

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def data(self):
        '''
        Return recent data as tuples
        '''
        return unicode(RECENT_DATA.get_datapoints())

    @cherrypy.expose
    def set(self, temp):
        if temp:
            # Set engine temp to new temp (using queue?)
            pass
        return 'Set temp to {0}'.format(temp)

class Interface(object):
    """
    Braubuddy web interface.
    """

    @cherrypy.expose
    def index(self):
        '''
        Serve html w/cur temp and status
        Serve garph js pointing at api
        '''
        return 'Braubuddy'

def main():
    '''
    Start the braubuddy engine and interface
    '''

    # Load global config and mount applications
    cherrypy.config.update(CONFIG_BRAUBUDDY)
    cherrypy.tree.mount(Interface(), '', config=CONFIG_BRAUBUDDY)
    cherrypy.tree.mount(API(), '/api', config=CONFIG_API)

    # Load engine config and initialise engine
    units = cherrypy.tree.apps[''].config['engine']['units']
    frequency = cherrypy.tree.apps[''].config['engine']['frequency']
    thermometer = cherrypy.tree.apps[''].config['engine']['thermometer']
    envcontroller = cherrypy.tree.apps[''].config['engine']['envcontroller']
    thermostat = cherrypy.tree.apps[''].config['engine']['thermostat']
    # Adding outputs to engine for now but this doesn't feel quite right
    # Should make outputs separate (custom plugin?) and event-driven
    outputs = cherrypy.tree.apps[''].config['outputs']
    outputs['recent_data'] = RECENT_DATA
    bb_engine = engine.Engine(envcontroller, thermometer, thermostat, outputs)

    # Create job to regularly perform thermostat cycle
    cycle = Monitor(cherrypy.engine, bb_engine.cycle,
        frequency=frequency, name='bb_engine')
    cycle.subscribe()

    # Start cherrypy
    cherrypy.engine.signals.subscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()
    return 0

if __name__ == '__main__':
    sys.exit(main())
