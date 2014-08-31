"""
Braubuddy Dummy thermometer unit tests.
"""

from mock import patch, call, MagicMock
from braubuddy.tests import BraubuddyTestCase
from braubuddy.thermometer import dummy 

class TestDummy(BraubuddyTestCase):

    def test_created_within_bounds(self):
        """Dummy thermometer is created and returns values within bounds."""

        lower_bound = 20
        upper_bound = 30
        allowed_range = range(lower_bound, upper_bound)
        test_dummy = dummy.DummyThermometer(
            lower_bound = lower_bound,
            upper_bound = upper_bound)
        for i in range(0,1000):
            self.assertIn(test_dummy.get_temperature(), allowed_range)
