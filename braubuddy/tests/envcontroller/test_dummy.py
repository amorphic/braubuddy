"""
Braubuddy Dummy envcontroller unit tests.
"""

from braubuddy.tests import BraubuddyTestCase
from braubuddy.envcontroller import dummy 
from braubuddy.envcontroller import PercentageError 


class TestDummy(BraubuddyTestCase):

    def test_heat_set_and_get(self):
        """Dummy device returns previously set heating value."""

        envcontroller = dummy.DummyEnvController()
        for i in range(0,100):
            envcontroller.set_heater_level(i)
            self.assertEqual(envcontroller.get_power_levels()[0], i)

    def test_cool_set_and_get(self):
        """Dummy device returns previously set cooling value."""

        envcontroller = dummy.DummyEnvController()
        for i in range(0,100):
            envcontroller.set_cooler_level(i)
            self.assertEqual(envcontroller.get_power_levels()[1], i)

    def test_heat_set_invalid(self):
        """Dummy device raises a PercentageError on invalid heating value."""
        envcontroller = dummy.DummyEnvController()
        with self.assertRaises(PercentageError):
            envcontroller.set_heater_level(101)

    def test_cool_set_invalid(self):
        """Dummy device raises a PercentageError on invalid cooling value."""
        envcontroller = dummy.DummyEnvController()
        with self.assertRaises(PercentageError):
            envcontroller.set_cooler_level(101)
