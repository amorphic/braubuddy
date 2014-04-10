"""
Braubuddy Environment Controller.
"""

import tosr0x
import abc
import logging

LOGGER = logging.getLogger(__name__)


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
    :mod:`braudbuddy`.
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
        """

    @abc.abstractmethod
    def set_cooler_level(percent):
        """
        Set environmental controller's cooler power level as a percentage of
        full power.
        
        :param percent: Cooler power level.
        :type _percent: :class:`int` in range(0-100)
        """

    @abc.abstractmethod
    def get_power_levels(self):
        """
        Get heater and cooler power levels.
        
        :returns: Heater and cooler power levels
        :rtype: :class:`tuple` of (:class:`int` <heater_power_level>,
            :class:`int` <cooler_power_level>)
        """

class DummyEnvController(IEnvController):
    """
    A dummy EnvController. Use for testing.
    """

    def __init__(self): 

        self._heater_percent = 0
        self._cooler_percent = 0

    def set_heater_level(self, percent):

        self._heater_percent = percent

    def set_cooler_level(self, percent):

        self._cooler_percent = percent

    def get_power_levels(self):

        return (self._heater_percent, self._cooler_percent)

class Tosr0xEnvController(IEnvController):
    """
    An environment controller utilising the Tosr0x family of relay modules: 
    
    <link>

    Uses relay 0 to switch heating and relay 1 to switch cooling. 

    :raises: :class:`braubuddy.envcontroller.DeviceError` if no Tosr0x USB relay
    module devices discovered.
    """

    def __init__(self, device_path=False):
        tosr0x_devices = self._get_tosr0x_devices()
        if len(tosr0x_devices) == 0:
            msg = 'No TEMPer USB devices discovered'
            LOGGER.error(msg)
            raise DeviceError(msg)
        # Use first device if multiple devices discovered
        self._tosr0x_device = tosr0x_devices[0]

    def _get_tosr0x_devices(self):
        """
        Internal method.

        Get attached Tosr0x devices
                        
        :returns: list of attached Tosr0x devices
        :rtype: :class:`list` of :class:`tosr0x.relayModule`
        """

        LOGGER.info('Discovering TEMPer USB thermometer(s)')   
        tosr0x_devices = tosr0x.handler()
        LOGGER.info(
            (
                '{0} TEMPer USB thermometer(s) '
                'discovered'
            ).format(len(tosr0x_devices))
        )   
        return tosr0x_devices

    def _set_relay_from_percent(self, relay_number, percent):
        """
        Internal method.

        Set given relay number state based on percent value. Percentage is
        converted to either on (0%) or off (1-100%).

        :param relay_number: The number of the relay to set.
        :type relay_number: :class:`float`
        :param percent: Power percentage. Converted to either on (0%) or off
            (0-100%).
        :type percent: Float
        :raises: :class:`envcontroller.PercentageError` if percent is not in
            the range 0-100.
        """

        if percent not in range(0,101):
            msg = '{0} is not in range 0-100'.format(percent)
            raise PercentageError(msg)
        if percent == 0:
            # 0 percent means off
            relay_state = 0
        else:
            # 1 - 100 pecent means on
            relay_state = 1

        self._tosr0x_device.set_relay_position(relay_number, relay_state)

    def set_heater_level(self, percent):

        self._set_relay_from_percent(1, percent)    

    def set_cooler_level(self, percent):

        self._set_relay_from_percent(2, percent)

    def get_power_levels(self):

        # Get relay states
        relay_states = self._tosr0x_device.get_relay_positions()

        # Convert 0/1 to percentage
        heater = 100 * (relay_states[1])
        cooler = 100 * (relay_states[2])
        return (heater, cooler)
