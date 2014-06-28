'''
Braubuddy thermostat interface.
'''

import abc


class IThermostat(object):
    """
    Interface for creating a thermostat for use with :mod:`braudbuddy`.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, target, units):
        """
        Initialise thermostat.

        :param target: Target temperature.
        :type target: :class:`float`
        :param units: Temperature units in which to work. Use 'celsius'
            or 'fahrenheit'.
        :type unit: :class:`str`
        """
    
        self._target = target
        self._units = units

    def get_target(self):
        return self._target

    def set_target(self, target):
        self._target = target

    def get_units(self):
        return self._units

    def set_units(self, units):
        self._units = units

    @abc.abstractmethod
    def get_required_state(self, temp, heater_percent, cooler_percent):
        """
        Get the required heater + cooler power levels given the current
        temperature and heater + cooler power levels.

        This is the thermostat's brain. Implement a clever and novel algorithm
        here.

        :param temp: Current temperature.
        :type temp: :class:`float`
        :param heater_percent: Current heater power level.
        :type heater_percent: :class:`int` in range(0-100)
        :param cooler: Current cooler power level.
        :type cooler: :class:`int` in range (0-100)
        :returns: Required heater and cooler power levels.
        :rtype: :class:`tuple` of (:class:`int`, :class:`int`)
        """
        pass
