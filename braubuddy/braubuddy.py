"""
Braubuddy

TODO:
- code layout
 - outputs need a better home
 - provide heavily commented config.example and tell users to copy it
- jinja2 template
 - basic template
 - graphs/graphics consuming api
- graphite output
"""
import os
import sys
import logging
import cherrypy
import json
import jinja2
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from cherrypy.process.plugins import Monitor

import thermostat
import thermometer
import envcontroller
import output
import engine

# Temp/Controller data
RECENT_DATA = output.ListMemory()

# Config files
#THIS_DIR = os.path.dirname(__file__)
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(THIS_DIR, 'config')
CONFIG_BRAUBUDDY = os.path.join(CONFIG_DIR, 'braubuddy')
CONFIG_API = os.path.join(CONFIG_DIR, 'api')
TEMPLATE_DIR = os.path.join(THIS_DIR, 'templates')

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

    def __init__(self):
        self.j2env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    @cherrypy.expose
    def index(self):
        '''
        Serve html w/cur temp and status
        Serve garph js pointing at api
        '''
        try:
            last_datapoint = RECENT_DATA.get_datapoints()[0]
            temp, heat, cool, time = RECENT_DATA.get_datapoints()[-1]
        except IndexError:
            # No datapoints loaded yet
            temp = 0
            heat = 0
            cool = 0
            time = 0
        time = datetime.fromtimestamp(time).strftime('%d-%m-%y %H:%M')
        template = self.j2env.get_template('braubuddy.html')
        print 'temp is ' + str(temp)
        return template.render(temp=temp, heat=heat, cool=cool, time=time)

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
