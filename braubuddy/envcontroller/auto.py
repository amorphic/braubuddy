from cherrypy import log
from braubuddy.envcontroller import DeviceError
from braubuddy.envcontroller import IEnvController
from braubuddy.envcontroller import Tosr0xEnvController
from braubuddy.envcontroller import DummyEnvController


class AutoEnvController(IEnvController):
    """
    Attempts to automatically discover a connected environmental controller
    device.

    * If mutliple devices are connected, the first discovered device is
        returned.
    * If no devices are detected, a dummy device is returned.
    """

    def __new__(self):
        """
        Return an instance of the first subclass of
        :class:`braubuddy.envcontroller.IEnvController` for which a device is
        discovered.
        """

        log('Auto-discovering Environmental Controller.')
        try:
            envcontroller = Tosr0xEnvController()
            log('Tosr0x Environmental Controller detected.')
            return envcontroller
        except DeviceError:
            log('No Tosr0x Environmental Controllers detected.')
        log.error(
            'No compatible Environmental Controllers detected. '
            'Using Dummy device.')
        return(DummyEnvController())
