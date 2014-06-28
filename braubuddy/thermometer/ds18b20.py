import logging
import ds18b20
from braubuddy.thermometer import DeviceError
from braubuddy.thermometer import IThermometer

LOGGER = logging.getLogger(__name__)


class DS18B20Thermometer(IThermometer):
    """
    A DS18B20 Thermometer

    :raises: :class:`braubuddy.thermometer.DeviceError` if no DS18B20
        thermometer devices discovered.
    """

    def __init__(self):
        try:
            self._ds18b20_device = ds18b20.DS18B20()
        except DS18B20Error as err:
            LOGGER.debug(err)
            raise DeviceError(err)

    def get_temperature(self, units='celsius'):
        try:
            # TODO: get temp in specified units
	        return self._ds18b20_device.get_temperature()
        except Exception as err:
            raise ReadError(
                'Error reading device temperature: {0}'.format(err))
