from cherrypy import log
from braubuddy.thermometer import DeviceError
from braubuddy.thermometer import IThermometer
from braubuddy.thermometer import DS18B20Thermometer
from braubuddy.thermometer import TEMPerThermometer
from braubuddy.thermometer import DummyThermometer


class AutoThermometer(IThermometer):
    """
    Attempts to automatically discover a connected thermometer device.

        * If mutliple devices are connected, the first discovered device is
            returned.
        * If no devices are detected, a dummy device is returned.
    """

    def __new__(self):
        """
        Return an instance of the first subclass of
        :class:`braubuddy.thermometer.IThermometer` for which a device is
        discovered.
        """

        log('Auto-discovering Thermometer.')
        try:
            thermometer = DS18B20Thermometer()
            log('DS18B20 Thermometer detected.')
            return thermometer
        except DeviceError:
            pass
            log('No DS18B20 Thermometers detected.')
        try:
            thermometer = TEMPerThermometer()
            log('TEMPer Thermometer detected.')
            return thermometer
        except DeviceError:
            log('No TEMPer Thermometers detected.')
        log.error('No compatible Thermometers detected. Using Dummy device.')
        return(DummyThermometer())
