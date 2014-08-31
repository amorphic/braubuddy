# -*- coding: utf-8 -*-
"""
Braubuddy Base unit tests
"""

from braubuddy.tests import BraubuddyTestCase
from braubuddy.output import base 


class IOutput(BraubuddyTestCase):

    def test_map_c_to_symbol(self):
        """c is mapped to °C"""
        self.assertEqual(
            base.IOutput.map_temp_units_to_symbol('c'), '°C')

    def test_map_C_to_symbol(self):
        """C is mapped to °C"""
        self.assertEqual(
            base.IOutput.map_temp_units_to_symbol('C'), '°C')

    def test_map_celsius_to_symbol(self):
        """celsius is mapped to °C"""
        self.assertEqual(
            base.IOutput.map_temp_units_to_symbol('celsius'), '°C')

    def test_map_c_to_symbol(self):
        """Celsius is mapped to °C"""
        self.assertEqual(
            base.IOutput.map_temp_units_to_symbol('Celsius'), '°C')

    def test_map_f_to_symbol(self):
        """f is mapped to °F"""
        self.assertEqual(
            base.IOutput.map_temp_units_to_symbol('f'), '°F')

    def test_map_F_to_symbol(self):
        """F is mapped to °F"""
        self.assertEqual(
            base.IOutput.map_temp_units_to_symbol('F'), '°F')

    def test_map_fahrenheit_to_symbol(self):
        """fahrenheit is mapped to °F"""
        self.assertEqual(
            base.IOutput.map_temp_units_to_symbol('fahrenheit'), '°F')

    def test_map_Fahrenheit_to_symbol(self):
        """Fahrenheit is mapped to °F"""
        self.assertEqual(
            base.IOutput.map_temp_units_to_symbol('Fahrenheit'), '°F')
