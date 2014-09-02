"""
Braubuddy envcontroller exceptions and interface.
"""

import abc
from cherrypy import log


class DeviceError(Exception):
    """
    Raised if there is a problem communicating with an environmental control
    device.
    """
    pass


class PercentageError(Exception):
    """
    Raised when a percentage is passed not in the range 0-100
    """


class IEnvController(object):
    """
    Interface for creating an environmental controller for use with
    :mod:`braubuddy`.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def set_heater_level(percent):
        """
        Set environmental controller's heater power level as a percentage of
        full power.

        :param percent: Heater power level.
        :type _percent: :class:`int` in range(0-100)
        :raises: PercentageError if percent is invalid
        """

    @abc.abstractmethod
    def set_cooler_level(percent):
        """
        Set environmental controller's cooler power level as a percentage of
        full power.

        :param percent: Cooler power level.
        :type _percent: :class:`int` in range(0-100)
        :raises: PercentageError if percent is invalid
        """

    @abc.abstractmethod
    def get_power_levels(self):
        """
        Get heater and cooler power levels.

        :returns: Heater and cooler power levels
        :rtype: :class:`tuple` of (:class:`int` <heater_power_level>,
            :class:`int` <cooler_power_level>)
        """
