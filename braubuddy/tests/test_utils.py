# -*- coding: utf-8 -*-
"""
Braubuddy utils unit tests
"""

from braubuddy.tests import BraubuddyTestCase
from braubuddy import utils

class TestAbbreviateTempUnits(BraubuddyTestCase):

    def test_abbreviate_celsius(self):
        """Celsisus is abbreviated to C"""
        self.assertEquals(utils.abbreviate_temp_units('Celsius'), 'C')
        self.assertEquals(utils.abbreviate_temp_units('celsius'), 'C')

    def test_abbreviate_fahrenheit(self):
        """Fahrenheit is abbreviated to F"""
        self.assertEquals(utils.abbreviate_temp_units('Fahrenheit'), 'F')
        self.assertEquals(utils.abbreviate_temp_units('fahrenheit'), 'F')

    def test_unknown_units(self):
        """Unknown units cannot be abbreviated"""
        with self.assertRaises(KeyError):
            utils.abbreviate_temp_units('invalid')

class TestConvertTempUnits(BraubuddyTestCase):

    def test_convert_celsius_to_fahrenheit(self):
        """Celsisus is converted to fahrenheit"""
        self.assertEquals(
            utils.convert_temp_units(20.0, 'celsius', 'fahrenheit'), 68.0)

    def test_convert_fahrenheit_to_celsius(self):
        """Fahrenheit is converted to celsius"""
        self.assertEquals(
            utils.convert_temp_units(68.0, 'fahrenheit', 'celsius'), 20.0)

    def test_unknown_from_units(self):
        """Unknown units cannot be converted from"""
        with self.assertRaises(KeyError):
            utils.convert_temp_units(68.0, 'invalid', 'celsius')

    def test_unknown_to_units(self):
        """Unknown units cannot be converted from"""
        with self.assertRaises(KeyError):
            utils.convert_temp_units(68.0, 'fahrenheit', 'invalid')

class TestMapTempUnitsToSymbol(BraubuddyTestCase):

    def test_map_celsius(self):
        units = ['celsius', 'Celsius', 'c', 'C']
        for unit in units:
            self.assertEqual(utils.map_temp_units_to_symbol(unit), '°C')

    def test_map_C(self):
        units = ['fahrenheit', 'Fahrenheit', 'f', 'F']
        for unit in units:
            self.assertEqual(utils.map_temp_units_to_symbol(unit), '°F')
