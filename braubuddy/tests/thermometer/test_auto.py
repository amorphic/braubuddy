"""
Braubuddy Auto thermometer unit tests.
"""

from mock import patch, call, MagicMock
from braubuddy.tests import BraubuddyTestCase
from braubuddy.thermometer import auto 
from braubuddy.thermometer import dummy 
from braubuddy.thermometer import ds18b20_gpio 
from braubuddy.thermometer import temper_usb 

class TestAuto(BraubuddyTestCase):

    @patch('braubuddy.thermometer.ds18b20_gpio.ds18b20')
    @patch('braubuddy.thermometer.temper_usb.temperusb')
    def test_dummy_returned_if_no_devices(self, mk_temperusb, mk_ds18b20):
        """Dummy thermometer is created if no real thermometers discovered."""

        mk_ds18b20.DS18B20 = MagicMock(side_effect = Exception('Some Error'))
        mk_temperusb.TemperHandler.return_value.get_devices.return_value = []
        thermometer = auto.AutoThermometer()
        self.assertIsInstance(thermometer, dummy.DummyThermometer)
