import logging
import cherrypy
import jinja2
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import braubuddy

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
        return unicode(braubuddy.RECENT_DATA.get_datapoints())

    @cherrypy.expose
    def set(self, temp):
        if temp:
            # Set components temp to new temp (using queue?)
            pass
        return 'Set temp to {0}'.format(temp)

class Dashboard(object):
    """
    Braubuddy Dashboard.
    """

    def __init__(self):
        self.j2env = Environment(loader=FileSystemLoader(braubuddy.TEMPLATE_DIR))

    @cherrypy.expose
    def index(self):
        '''
        Serve html w/cur temp and status
        Serve garph js pointing at api
        '''
        try:
            last_datapoint = braubuddy.RECENT_DATA.get_datapoints()[0]
            temp, heat, cool, time = braubuddy.RECENT_DATA.get_datapoints()[-1]
        except IndexError:
            # No datapoints loaded yet
            temp = 0
            heat = 0
            cool = 0
            time = 0
        time = datetime.fromtimestamp(time).strftime('%d-%m-%y %H:%M')
        template = self.j2env.get_template('braubuddy.html')
        return template.render(temp=temp, heat=heat, cool=cool, time=time)

class Engine(object):
    """
    Braubuddy Engine.
    """

    def cycle(self):
        """
        Perform full thermostat cycle and return state.
        """
        
        envcontroller = cherrypy.request.app.config['components']['envcontroller']
        thermometer = cherrypy.request.app.config['components']['thermometer']
        thermostat = cherrypy.request.app.config['components']['thermostat']
        
        # Environment input
        ## Catch exceptions. Retries in thermometer.
        current_heat, current_cool = envcontroller.get_power_levels()
        current_temp = thermometer.get_temperature()
        required_heat, required_cool = thermostat.get_required_state(
            current_temp, current_heat, current_cool)

        # Set power levels
        envcontroller.set_heater_level(required_heat)
        envcontroller.set_cooler_level(required_cool)

        # Output
        # Should work out a way of doing this outside the components
        outputs = cherrypy.request.app.config['outputs']
        for name, output in outputs.iteritems():
            output.publish_status(current_temp, current_heat, current_cool)
