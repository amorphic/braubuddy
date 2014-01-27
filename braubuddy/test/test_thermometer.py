'''
Braubuddy thermometer unit tests
'''

import thermometer
import unittest

class TestRandomRangeThermometer(unittest.TestCase):

    def test_within_bounds(self):
        lower_bound = 20
        upper_bound = 30
        test_thermometer = thermometer.RandomRangeThermometer(
            lower_bound = lower_bound,
            upper_bound = upper_bound
        )
        for i in range(0,1000):
            temp = test_thermometer.get_temperature()
            self.assertIn(
                temp,
                range(
                    lower_bound,
                    upper_bound
                )
            )
