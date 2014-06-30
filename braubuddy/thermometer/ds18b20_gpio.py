from cherrypy import log
import ds18b20
from braubuddy.thermometer import DeviceError
from braubuddy.thermometer import ReadError
from braubuddy.thermometer import IThermometer


class DS18B20Thermometer(IThermometer):
    """
    A DS18B20 Thermometer.

    :raises: :class:`braubuddy.thermometer.DeviceError` if no DS18B20
        thermometer devices discovered.
    """

    def __init__(self):
        try:
            self._ds18b20_device = ds18b20.DS18B20()
        except Exception as err:
            msg = 'No DS18B20 devices discovered'
            raise DeviceError(msg)

    def get_temperature(self, units='celsius'):
        try:
            # TODO: get temp in specified units
	        return self._ds18b20_device.get_temperature()
        except Exception as err:
            raise ReadError(
                'Error reading device temperature: {0}'.format(err))
