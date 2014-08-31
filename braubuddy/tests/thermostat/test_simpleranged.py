"""
Braubuddy SimpleRanged thermostat unit tests
"""

from braubuddy.tests import BraubuddyTestCase
from braubuddy.thermostat import simpleranged

class TestSimpleRangedInvalidBounds(BraubuddyTestCase):

    def test_upper_inside_equals_upper_outside(self):
        """Upper inside bound equals upper outside bound"""
        with self.assertRaises(ValueError):
            thermostat = simpleranged.SimpleRangedThermostat(20, lower_out=2,
                lower_in=1, upper_in=1, upper_out=1)

    def test_upper_inside_gt_upper_outside(self):
        """Upper inside bound greater than upper outside bound"""
        with self.assertRaises(ValueError):
            thermostat = simpleranged.SimpleRangedThermostat(20, lower_out=2,
                lower_in=1, upper_in=2, upper_out=1)

    def test_lower_inside_equals_lower_outside(self):
        """Lower inside bound equals lower outside bound"""
        with self.assertRaises(ValueError):
            thermostat = simpleranged.SimpleRangedThermostat(20, lower_out=1,
                lower_in=1, upper_in=1, upper_out=2)

    def test_lower_inside_gt_lower_outside(self):
        """Lower inside bound greater than lower outside bound"""
        with self.assertRaises(ValueError):
            thermostat = simpleranged.SimpleRangedThermostat(20, lower_out=1,
                lower_in=2, upper_in=2, upper_out=1)


class TestSimpleRangedRequiredStates(BraubuddyTestCase):

    def setUp(self):
        target = 20
        units =  'celsius'
        self.thermostat = simpleranged.SimpleRangedThermostat(
            target,
            lower_out=2,
            lower_in=1,
            upper_in=1,
            upper_out=2
        )
            
    def test_temp_within_inner_bounds(self):
        """Heating/Cooling off if temp within upper_in and lower_in bounds."""
        t = 20
        h = 100
        c = 0
        r = (0, 0)
        self.assertEqual(self.thermostat.get_required_state(t, h, c), r)

    def test_temp_within_upper_bounds(self):
        """Heating/Cooling unchanged if temp within upper bounds."""
        t = 21.5
        h = 0
        c = 100
        r = (0, 100)
        self.assertEqual(self.thermostat.get_required_state(t, h, c), r)

    def test_temp_within_lower_bounds(self):
        """Heating/Cooling unchanged if temp within lower bounds."""
        t = 18.5
        h = 100
        c = 0
        r = (100, 0)
        self.assertEqual(self.thermostat.get_required_state(t, h, c), r)

    def test_temp_exceeds_upper_outer_bound(self):
        """Cooling turned on if temp exceeds upper outer bound."""
        t = 22.5
        h = 0
        c = 0
        r = (0, 100)
        self.assertEqual(self.thermostat.get_required_state(t, h, c), r)

    def test_temp_exceeds_lower_outer_bound(self):
        """Heating turned on if temp exceeds lower outer bound."""
        t = 17.5
        h = 0
        c = 0
        r = (100, 0)
        self.assertEqual(self.thermostat.get_required_state(t, h, c), r)
