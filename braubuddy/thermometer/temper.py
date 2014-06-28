import logging
import temperusb
from braubuddy.thermometer import DeviceError
from braubuddy.thermometer import IThermometer

LOGGER = logging.getLogger(__name__)


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
        :rtype: :class:`list` of :class:`temperusb.TemperDevice`
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
            # TODO: get temp in specified units
	        return self._temper_device.get_temperature()
        except Exception as err:
            raise ReadError(
                'Error reading device temperature: {0}'.format(err))
