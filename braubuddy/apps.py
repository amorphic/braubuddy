import logging
import cherrypy
import jinja2
import time
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
    def status(self, **kwargs):
        '''
        Return recent data as tuples
        '''
        try:
            since = int(kwargs.get('since', 0))
        except ValueError:
            since = 0
        try:
            before = int(kwargs.get('before', 0))
        except ValueError:
            before = 0
        try:
            limit = int(kwargs.get('limit', 0))
        except ValueError:
            limit = 0
        return braubuddy.RECENT_DATA.get_datapoints(
                since=since, before=before, limit=limit)

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
        ##TODO: components = cherrypy.request.app.config['components']
        ##target = components['thermometer'].get_target_temp()
        target = 21
        units = 'C'
        try:
            last_datapoint = braubuddy.RECENT_DATA.get_datapoints()[0]
            temp, heat, cool, time = braubuddy.RECENT_DATA.get_datapoints()[-1]
        except IndexError:
            # No datapoints loaded yet
            temp = 0
            heat = 0
            cool = 0
            time = 0
        time = datetime.fromtimestamp(time).strftime('%H:%M')
        template = self.j2env.get_template('braubuddy.html')
        return template.render(temp=temp, heat=heat, cool=cool, time=time,
                target=target, units=units)

class Engine(object):
    """
    Braubuddy Engine.
    """

    def cycle(self):
        """
        Perform full thermostat cycle and return state.
        """

        retries = cherrypy.request.app.config['components']['retries']
        retry_delay = cherrypy.request.app.config['components']['retry_delay']
        envcontroller = cherrypy.request.app.config['components']['envcontroller']
        thermometer = cherrypy.request.app.config['components']['thermometer']
        thermostat = cherrypy.request.app.config['components']['thermostat']
        
        # Environment input
        current_heat, current_cool = envcontroller.get_power_levels()

        # Temperature input
	for i in range(retries):
            try:
                current_temp = thermometer.get_temperature()
                break
	    except braubuddy.thermometer.ReadError, err:
		cherrypy.request.app.log.error(err.message)
            time.sleep(retry_delay)
	else:
	    cherrypy.request.app.log.error(
                'Unable to collect temperature after {0} '
		'tries'.format(retries))
	    return False
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
	return True
