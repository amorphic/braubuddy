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
    @cherrypy.tools.json_out()
    def index(self, **kwargs):
        """
        Return recent status data as tuples.
        """
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
        """
        Set target temperature.
        """
        if temp:
            # Set components temp to new temp.
            # TODO: Implement this when auth functionality exists for API.
            pass
        return 'Temperature set to {0}'.format(temp)


class Dashboard(object):
    """
    Braubuddy Dashboard.
    """

    def __init__(self):
        self.j2env = Environment(
            loader=FileSystemLoader(braubuddy.TEMPLATE_DIR))

    @cherrypy.expose
    def index(self):
        '''
        Braubuddy dashboard displaying:
            * current temperature
            * current heat level
            * current cool level
            * target temperature
            * last cycle time
            * hourly temperature chart
            * daily temperature chart
        '''
        template = self.j2env.get_template('braubuddy.html')
        return template.render(
            title=cherrypy.config['dashboard_title'],
            frequency=cherrypy.config['frequency'],
            units=braubuddy.utils.abbreviate_temp_units(
                cherrypy.config['units']),
            show_footer=cherrypy.config['dashboard_footer'],
            year=datetime.now().year,
        )


class Engine(object):
    """
    Braubuddy Engine.
    """

    def cycle(self):
        """
        Perform full thermostat cycle and return state.
        """

        units = cherrypy.config['units']
        retry_count = cherrypy.config['retry_count']
        retry_delay = cherrypy.config['retry_delay']
        envcontroller = cherrypy.config['envcontroller']
        thermometer = cherrypy.config['thermometer']
        thermostat = cherrypy.config['thermostat']
        # Environment input
        current_heat, current_cool = envcontroller.get_power_levels()
        # Temperature input
        for i in range(retry_count):
            try:
                current_temp = thermometer.get_temperature(units=units)
                break
            except braubuddy.thermometer.ReadError as err:
                cherrypy.log.error(err.message)
                time.sleep(retry_delay)
        else:
            cherrypy.request.app.log.error(
                'Unable to collect temperature after {0} '
                'tries'.format(retry_count))
            return False
        # Set power levels
        required_heat, required_cool = thermostat.get_required_state(
            current_temp, current_heat, current_cool, units=units)
        envcontroller.set_heater_level(required_heat)
        envcontroller.set_cooler_level(required_cool)
        # Output
        target = thermostat.target
        for name, output in cherrypy.request.app.config['outputs'].iteritems():
            try:
                output.publish_status(target, current_temp, current_heat,
                                      current_cool)
            except braubuddy.output.OutputError as err:
                cherrypy.log.error(err.message)
        return True
