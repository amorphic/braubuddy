"""
Braubuddy Tosr0x envcontroller unit tests.
"""

from mock import patch, call, MagicMock
from braubuddy.tests import BraubuddyTestCase
from braubuddy.envcontroller import tosr0x_usb
from braubuddy.envcontroller import DeviceError 
from braubuddy.envcontroller import PercentageError 


@patch('braubuddy.envcontroller.tosr0x_usb.tosr0x')
class TestTosr0x(BraubuddyTestCase):

    def test_tosr0x_detected(self, mk_tosr0x):
        """Tosr0x device is detected if present."""
        mk_tosr0x_device = MagicMock()
        mk_tosr0x.handler.return_value = [mk_tosr0x_device]
        envcontroller = tosr0x_usb.Tosr0xEnvController()
        self.assertIs(envcontroller._tosr0x_device, mk_tosr0x_device)

    def test_first_if_multiple_tosr0x_detected(self, mk_tosr0x):
        """First Tosr0x device is detected if multiple present."""
        mk_tosr0x_device_1 = MagicMock()
        mk_tosr0x_device_2 = MagicMock()
        mk_tosr0x_device_3 = MagicMock()
        mk_tosr0x.handler.return_value = [ 
            mk_tosr0x_device_1,
            mk_tosr0x_device_2,
            mk_tosr0x_device_3,
        ]
        envcontroller = tosr0x_usb.Tosr0xEnvController()
        self.assertIs(envcontroller._tosr0x_device, mk_tosr0x_device_1)

    def test_tosr0x_not_detected(self, mk_tosr0x):
        """DeviceError raised if no Tosr0x devices present."""
        mk_tosr0x.handler.return_value = []
        with self.assertRaises(DeviceError):
            t = tosr0x_usb.Tosr0xEnvController()

    def test_heat_set_zero(self, mk_tosr0x):
        """Tosr0x device heater relay (#1) switched off when heat == 0."""
        mk_tosr0x_device = MagicMock()
        mk_tosr0x.handler.return_value = [mk_tosr0x_device]
        envcontroller = tosr0x_usb.Tosr0xEnvController()
        envcontroller.set_heater_level(0)
        mk_tosr0x_device.set_relay_position.assert_called_with(1, 0)

    def test_heat_set_gt_zero(self, mk_tosr0x):
        """Tosr0x device heater relay (#1) switched on when heat > 0."""
        mk_tosr0x_device = MagicMock()
        mk_tosr0x.handler.return_value = [mk_tosr0x_device]
        envcontroller = tosr0x_usb.Tosr0xEnvController()
        for h in range(1, 101):
            envcontroller.set_heater_level(h)
            mk_tosr0x_device.set_relay_position.assert_called_with(1, 1)   

    def test_cool_set_zero(self, mk_tosr0x):
        """Tosr0x device cooler relay (#2) switched off when cool == 0."""
        mk_tosr0x_device = MagicMock()
        mk_tosr0x.handler.return_value = [mk_tosr0x_device]
        envcontroller = tosr0x_usb.Tosr0xEnvController()
        envcontroller.set_cooler_level(0)
        mk_tosr0x_device.set_relay_position.assert_called_with(2, 0)

    def test_cool_set_gt_zero(self, mk_tosr0x):
        """Tosr0x device cooler relay (#2) switched on when cool > 0."""
        mk_tosr0x_device = MagicMock()
        mk_tosr0x.handler.return_value = [mk_tosr0x_device]
        envcontroller = tosr0x_usb.Tosr0xEnvController()
        for h in range(1, 101):
            envcontroller.set_cooler_level(h)
            mk_tosr0x_device.set_relay_position.assert_called_with(2, 1)   

    def test_get_power_levels_100_percent(self, mk_tosr0x):
        """Tosr0x device returns heating/cooling 100% when both relays on."""
        mk_tosr0x_device = MagicMock()
        relays_both_on = {1:1, 2:1}
        mk_tosr0x_device.get_relay_positions.return_value = relays_both_on
        mk_tosr0x.handler.return_value = [mk_tosr0x_device]
        envcontroller = tosr0x_usb.Tosr0xEnvController()
        self.assertEqual(envcontroller.get_power_levels(), (100, 100))

    def test_get_power_levels_0_percent(self, mk_tosr0x):
        """Tosr0x device returns heating/cooling 0% when both relays off."""
        mk_tosr0x_device = MagicMock()
        relays_both_on = {1:0, 2:0}
        mk_tosr0x_device.get_relay_positions.return_value = relays_both_on
        mk_tosr0x.handler.return_value = [mk_tosr0x_device]
        envcontroller = tosr0x_usb.Tosr0xEnvController()
        self.assertEqual(envcontroller.get_power_levels(), (0, 0))

    def test_heat_set_invalid(self, mk_tosr0x):
        """Tosr0x device raises a PercentageError on invalid heating value."""
        mk_tosr0x_device = MagicMock()
        mk_tosr0x.handler.return_value = [mk_tosr0x_device]
        envcontroller = tosr0x_usb.Tosr0xEnvController()
        with self.assertRaises(PercentageError):
            envcontroller.set_heater_level(101)

    def test_cool_set_invalid(self, mk_tosr0x):
        """Tosr0x device raises a PercentageError on invalid cooling value."""
        mk_tosr0x_device = MagicMock()
        mk_tosr0x.handler.return_value = [mk_tosr0x_device]
        envcontroller = tosr0x_usb.Tosr0xEnvController()
        with self.assertRaises(PercentageError):
            envcontroller.set_cooler_level(101)
