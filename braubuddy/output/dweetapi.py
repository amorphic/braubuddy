from datetime import datetime
import dweepy
from braubuddy.output import IOutput
from braubuddy.output import OutputError


class DweetAPIOutput(IOutput):
    """
    Output to the `Dweet <http://dweet.io>`_ API.

    :param units: Temperature units to output. Use 'celsius' or
        'fahrenheit'.
    :type units: :class:`str`
    :param frequency: Minimum seconds between dweets.
    :type frequency: :class:`int`
    :param thing_name: Dweet thing name, Replace this with something unique.
    :type thing_name: :class:`str`
    """

    def __init__(self, units='celsius', frequency=86400,
                 thing_name='braubuddy'):

        self._frequency = frequency
        self._thing_name = thing_name
        self._last_published = datetime.now()
        super(DweetAPIOutput, self).__init__(units)

    def publish_status(self, target, temp, heater_percent, cooler_percent):

        if (datetime.now() - self._last_published).seconds < self._frequency:
            # Don't Dweet until the defined frequency has passed.
            return

        try:
            response = dweepy.dweet_for(
                self._thing_name,
                {
                    'temperature':  temp,
                    'target':       target,
                    'heater':       heater_percent,
                    'cooler':       cooler_percent,
                }
            )
        except Exception as err:
            raise OutputError(
                'Error publishing to Dweet API: {0}'.format(err))
        if response['this'] != 'succeeded':
            print response
            raise OutputError(
                'Error publishing to Dweet API: {0}'.format(response['this']))
        else:
            self._last_published = datetime.now()
