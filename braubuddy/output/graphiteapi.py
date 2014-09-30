import graphitesend 
from cherrypy import log
from braubuddy.output import IOutput
from braubuddy.output import OutputError


class GraphiteAPIOutput(IOutput):
    """
    Output to the `Graphite <http://metrics.librato.com>`_ API.

    :param units: Temperature units to output. Use 'celsius' or
        'fahrenheit'.
    :type units: :class:`str`
    :param host: Graphite service host name or IP address.
    :type host: :class:`str`
    :param port: Graphite service port.
    :type port: class:`int`
    :param prefix: Graphite metric prefix.
    :type prefix: :class:`str`
    """

    def __init__(self, units='celsius', host='graphite.example.com',
                 port=2003, prefix='braubuddy'):

        self._service = graphitesend.init(
            graphite_server=host,
            graphite_port=port,
            prefix=prefix,
            system_name='',
        )
        super(GraphiteServiceOutput, self).__init__(units)

    def publish_status(self, target, temp, heater_percent, cooler_percent):

        try:
            self._service.send_dict({
                'target_temp':      target,
                'actual_temp':      temp,
                'heater_percent':   heater_percent,
                'cooler_percent':   cooler_percent,
              })
        except Exception as err:
            raise OutputError(
                'Error publishing to Graphite service: {0}'.format(err))

