"""
Braubuddy Thermometer
"""

import random
import abc
import temperusb
import ds18b20
import logging
from usb import USBError

LOGGER = logging.getLogger(__name__)

def abbreviate_temp_units(units):
    """
    Abbreviate temperature full name to single letter.

    :param units: Temperature units to abbreviate.
    :type units: :class:`string`
    """
    conversion_map = {
        'celsius':      'C',
        'Celsius':      'C',
        'Farenheit':    'F',
        'farenheit':    'F',
    }
    if units not in conversion_map.keys():
        raise KeyError('Unable to abbreviate {0}. Unknown unit.'.format(units))
    return conversion_map[units]

def convert_temp_units(temperature, units_from='celsius', units_to='fahrenheit'):
    """
    Convert units of a given temperature value.

    :param temperature: Temperature value to convert.
    :type temperature: :class:`float`
    :param units_from: Temperature units to convert from.
    :type units_from: :class:`string`
    :param units_to: Temperature units to convert to.
    :type units_to: :class:`string`
    :returns: Converted temperature value.
    :rtype: :class:`float`
    """
    conversion_map = {
        'celsius':      {
            'fahrenheit':   lambda t: (9.0 / 5.0 * t) + 32,
            'celsius':      lambda t: t
        },   
        'fahrenheit':   {
            'celsius':      lambda t: (t - 32) * (5.0 / 9.0),
            'fahrenheit':   lambda t: t
        }
    }
    # Use lowercase units names to catch more input values
    units_from = units_from.lower()
    units_to = units_to.lower()
    if units_from not in conversion_map.keys():
        raise KeyError(
            'Unable to convert from {0!r} to {1!r}'.format(
                units_from,
                units_to
            )
        )
    conversion_sub_map = conversion_map[units_from]
    if units_to not in conversion_sub_map.keys():
        raise KeyError(
            'Unable to convert from {0!r} to {1!r}'.format(
                units_from,
                units_to
            )
        )
    return conversion_sub_map[units_to](temperature)

class DeviceError(Exception):
    """
    Raised if there is a problem communicating with a thermometer device.
    """
    pass

class ReadError(Exception):
    """
    Raised if there is a problem reading temperature.
    """
    pass

class IThermometer(object):
    """
    Interface for creating a thermometer for use with :mod:`braudbuddy`.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_temperature(self, units='celsius'):
        """
        Get thermometer temperature in celsius or farenheit.

        :param units: Temperature units, 'celsius' (default) or 'farenheit.'
        :type units: :class:`str` (either 'celsius' or 'farenheit').
        :returns: Thermometer temperature reading
        :rtype: :class:`float`
        :raises: :class:`braubuddy.thermometer.ReadError` if temperature can not
        be read.
        """
        pass

    
class DummyThermometer(IThermometer):
    """
    A dummy thermometer which generates random temperature readings within
    a defined range. Use for testing.

    :param `lower_bound`: Lower bound of returned temperature range
    :type `lower_bound`: :class:`int`
    :param `upper_bound`: Upper bound of returned temperature range
    :type `upper_bound`: :class:`int`
    """

    def __init__(self, lower_bound=20, upper_bound=30):
        # Set random range bounds
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        super(DummyThermometer, self).__init__()

    def get_temperature(self, units='celsius'):
        # Returns random temperature within defined range
        current_temp = random.randrange(self.lower_bound, self.upper_bound)
        if units == 'fahrenheit':
            current_temp = convert_temp_units(
                current_temp,
                units_from='celsius',
                units_to='fahrenheit'
            )
        return current_temp

class TemperThermometer(IThermometer):
    """
    A TEMPer USB Thermometer

    :raises: :class:`braubuddy.thermometer.DeviceError` if no TEMPer USB
    thermometer devices discovered.
    """

    def __init__(self):
        temper_devices = self._get_temper_devices()
        if len(temper_devices) == 0:
            msg = 'No TEMPer USB devices discovered'
            LOGGER.error(msg)
            raise DeviceError(msg)
        # Use first device if multiple devices discovered
        self._temper_device = temper_devices[0]

    def _get_temper_devices(self):
        """
        Internal method.

        Get attached TEMPer devices
        
        :returns: list of attached TEMPer devices
        :rtype: :class:`list` of :class:`temper.TemperDevice`
        """
        LOGGER.info(
            'Discovering TEMPer USB thermometer(s)'
        )
        th = temperusb.TemperHandler()
        temper_devices = th.get_devices()
        LOGGER.info(
            (
                '{0} TEMPer USB thermometer(s) '
                'discovered`'
            ).format(len(temper_devices))
        )
        return temper_devices

    def get_temperature(self, units='celsius'):
        try:
	        return self._temper_device.get_temperature()
        except Exception as err:
            raise ReadError(
                'Error reading device temperature: {0}'.format(err))


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
	        return self._ds18b20_device.get_temperature()
        except Exception as err:
            raise ReadError(
                'Error reading device temperature: {0}'.format(err))
