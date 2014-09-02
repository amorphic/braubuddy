"""
Braubuddy thermometer exceptions and interface.
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

    @abc.abstractmethod
    def get_temperature(self, units='celsius'):
        """
        Get thermometer temperature in celsius or farenheit.

        :param units: Temperature units, 'celsius' (default) or 'farenheit.'
        :type units: :class:`str`
        :returns: Thermometer temperature reading
        :rtype: :class:`float`
        :raises: :class:`braubuddy.thermometer.ReadError` if temperature can
            not be read.
        """
        pass
