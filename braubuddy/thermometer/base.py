"""
Braubuddy envcontroller exceptions and interface.
"""

import abc


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

    @staticmethod
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

    @staticmethod
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

    @abc.abstractmethod
    def get_temperature(self, units='celsius'):
        """
        Get thermometer temperature in celsius or farenheit.

        :param units: Temperature units, 'celsius' (default) or 'farenheit.'
        :type units: :class:`str`
        :returns: Thermometer temperature reading
        :rtype: :class:`float`
        :raises: :class:`braubuddy.thermometer.ReadError` if temperature can not
            be read.
        """
        pass
