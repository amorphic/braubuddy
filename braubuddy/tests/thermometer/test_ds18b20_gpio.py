"""
Braubuddy DS18B20 thermometer unit tests
"""

from mock import patch, call, MagicMock
from braubuddy.tests import BraubuddyTestCase
from braubuddy.thermometer import ds18b20_gpio
from braubuddy.thermometer import DeviceError
from braubuddy.thermometer import ReadError


@patch('braubuddy.thermometer.ds18b20_gpio.ds18b20')
class TestDS18B20(BraubuddyTestCase):
   
    def test_ds18b20_detected(self, mk_ds18b20):
        """DS18B20 device is detected if present."""
        mk_ds18b20_device = MagicMock()
        mk_ds18b20.DS18B20.return_value = mk_ds18b20_device
        thermometer = ds18b20_gpio.DS18B20Thermometer()
        self.assertIs(thermometer._ds18b20_device, mk_ds18b20_device)

    def test_ds18b20_not_detected(self, mk_ds18b20):
        """DS18B20 device is not detected if not present"""
        mk_ds18b20.DS18B20 = MagicMock(side_effect = Exception('Some Error'))
        with self.assertRaises(DeviceError):
            t = ds18b20_gpio.DS18B20Thermometer()

    def test_ds18b20_get_temp_celsius_default(self, mk_ds18b20):
        """DS18B20 device temperature is requested in celsius by default."""
        temp_c = 30
        mk_ds18b20_device = MagicMock()
        mk_ds18b20_device.get_temperature.return_value = temp_c
        mk_ds18b20.DS18B20.return_value = mk_ds18b20_device
        thermometer = ds18b20_gpio.DS18B20Thermometer()
        self.assertEqual(thermometer.get_temperature(), temp_c)
        mk_ds18b20_device.get_temperature.assert_called_with(unit=1)

    def test_ds18b20_get_temp_fahreheit(self, mk_ds18b20):
        """DS18B20 device temperature is requested in fahrenheit."""
        temp_f = 86
        mk_ds18b20_device = MagicMock()
        mk_ds18b20_device.get_temperature.return_value = temp_f
        mk_ds18b20.DS18B20.return_value = mk_ds18b20_device
        thermometer = ds18b20_gpio.DS18B20Thermometer()
        self.assertEqual(thermometer.get_temperature(units='fahrenheit'), temp_f)
        mk_ds18b20_device.get_temperature.assert_called_with(unit=2)

    def test_ds18b20_read_error(self, mk_ds18b20):
        """ReadError is raised on DS18B20 device read error."""
        mk_ds18b20_device = MagicMock()
        mk_ds18b20_device.get_temperature.side_effect = Exception('Some Error')
        mk_ds18b20.DS18B20.return_value = mk_ds18b20_device
        thermometer = ds18b20_gpio.DS18B20Thermometer()
        with self.assertRaises(ReadError):
            thermometer.get_temperature()
