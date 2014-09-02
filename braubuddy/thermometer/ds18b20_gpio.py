import ds18b20
from braubuddy.thermometer import DeviceError
from braubuddy.thermometer import ReadError
from braubuddy.thermometer import IThermometer

UNIT_MAP = {
    'celsius':      1,
    'fahrenheit':   2
}


class DS18B20Thermometer(IThermometer):
    """
    DS18B20 GPIO anagolgue thermometer manufactured by `Maxim
    Integrated Products <http://www.maximintegrated.com>`_.

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
            return self._ds18b20_device.get_temperature(unit=UNIT_MAP[units])
        except Exception as err:
            raise ReadError(
                'Error reading device temperature: {0}'.format(err))
