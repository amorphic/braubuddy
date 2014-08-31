"""
Braubuddy TEMPer thermometer unit tests
"""

from mock import patch, call, MagicMock
from braubuddy.tests import BraubuddyTestCase
from braubuddy.thermometer import temper_usb 
from braubuddy.thermometer import DeviceError
from braubuddy.thermometer import ReadError


@patch('braubuddy.thermometer.temper_usb.temperusb')
class TestTEMPer(BraubuddyTestCase):
   
    def test_temper_detected(self, mk_temperusb):
        """TEMPer device is detected if present."""
        mk_temper_device = MagicMock()
        mk_temperusb.TemperHandler.return_value.get_devices.return_value = \
            [mk_temper_device]
        thermometer = temper_usb.TEMPerThermometer()
        self.assertIs(thermometer._temper_device, mk_temper_device)

    def test_first_if_multiple_temper_detected(self, mk_temperusb):
        """First TEMPer device is detected if multiple present."""
        mk_temper_device_1 = MagicMock()
        mk_temper_device_2 = MagicMock()
        mk_temper_device_3 = MagicMock()
        mk_temperusb.TemperHandler.return_value.get_devices.return_value = [ 
            mk_temper_device_1,
            mk_temper_device_2,
            mk_temper_device_3,
        ]
        thermometer = temper_usb.TEMPerThermometer()
        self.assertIs(thermometer._temper_device, mk_temper_device_1)

    def test_temper_not_detected(self, mk_temperusb):
        """DeviceError raised if no TEMPer devices present."""
        mk_temperusb.TemperHandler.return_value.get_devices.return_value = []
        with self.assertRaises(DeviceError):
            t = temper_usb.TEMPerThermometer()

    def test_temper_get_temp_celsius_default(self, mk_temperusb):
        """TEMPer device temperature is requested in celsius by default."""
        temp_c = 30
        mk_temper_device = MagicMock()
        mk_temper_device.get_temperature.return_value = temp_c
        mk_temperusb.TemperHandler.return_value.get_devices.return_value = \
            [mk_temper_device]
        thermometer = temper_usb.TEMPerThermometer()
        self.assertEqual(thermometer.get_temperature(), temp_c)
        mk_temper_device.get_temperature.assert_called_with(format='celsius')

    def test_temper_get_temp_fahreheit(self, mk_temperusb):
        """TEMPer device temperature is requested in fahrenheit."""
        temp_f = 86
        mk_temper_device = MagicMock()
        mk_temper_device.get_temperature.return_value = temp_f
        mk_temperusb.TemperHandler.return_value.get_devices.return_value = \
            [mk_temper_device]
        thermometer = temper_usb.TEMPerThermometer()
        self.assertEqual(thermometer.get_temperature(units='fahrenheit'), temp_f)
        mk_temper_device.get_temperature.assert_called_with(format='fahrenheit')

    def test_temper_read_error(self, mk_temperusb):
        """ReadError is raised on TEMPer device read error."""
        mk_temper_device = MagicMock()
        mk_temper_device.get_temperature.side_effect=Exception('Some Error')
        mk_temperusb.TemperHandler.return_value.get_devices.return_value = \
            [mk_temper_device]
        thermometer = temper_usb.TEMPerThermometer()
        with self.assertRaises(ReadError):
            thermometer.get_temperature()
