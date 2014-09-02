import tosr0x
from braubuddy.envcontroller import IEnvController
from braubuddy.envcontroller import DeviceError
from braubuddy.envcontroller import PercentageError


class Tosr0xEnvController(IEnvController):
    """
    Tosr0x family of relay modules manufactured by
    `TinySine <http://www.tinyosshop.com>`_.

    Relay 0 switches heating and relay 1 switches cooling.

    :raises: :class:`braubuddy.envcontroller.DeviceError` if no Tosr0x USB
        relay module devices discovered.
    """

    def __init__(self, device_path=False):
        tosr0x_devices = self._get_tosr0x_devices()
        if len(tosr0x_devices) == 0:
            msg = 'No Tosr0x devices discovered'
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

        tosr0x_devices = tosr0x.handler()
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

        if percent not in range(0, 101):
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
