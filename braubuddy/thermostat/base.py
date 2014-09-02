'''
Braubuddy thermostat interface.
'''

import abc


class IThermostat(object):
    """
    Interface for creating a thermostat for use with :mod:`braudbuddy`.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, target):
        """
        Initialise thermostat.

        :param target: Target temperature.
        :type target: :class:`float`
        """

        self._target = target

    @property
    def target(self):
        """
        Get the target temperature.
        """
        return self._target

    @target.setter
    def target(self, target):
        self._target = target

    @abc.abstractmethod
    def get_required_state(self, temp, heater_percent, cooler_percent,
                           units='celsius'):
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
        :param units: Temperature units in which to work. Use 'celsius'
            or 'fahrenheit'.
        :type units: :class:`str`
        :returns: Required heater and cooler power levels.
        :rtype: :class:`tuple` of (:class:`int`, :class:`int`)
        """
        pass
