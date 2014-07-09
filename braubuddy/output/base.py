# -*- coding: utf-8 -*-
"""
Braubuddy output template and interface.
"""

import abc


class OutputError(Exception):
    """
    Raised whenever an output fails
    """

class IOutput(object):
    """
    Interface for creating an output for use with :mod:`braubuddy`.

    :param units: Temperature units to output.
    :type units: :class:`str`
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, units='celsius'):

        self.set_units(units)

    def set_units(self, new_units):
        """
        Set units to output.

        :param units: Temperature units to output.
        :type units: :class:`str`
        """

        try:
            self.units = self.map_temp_units_to_symbol(new_units)
        except:
            raise OutputError('Unrecognised units: {0}'.format(units))

    @staticmethod
    def map_temp_units_to_symbol(units='celsius'):
        """ 
        Map temperature units to a symbol for output.

        :param units: Temperature units to output. Use 'celsius' or
            'fahrenheit'.
        :type units: :class:`str`
        """

        unit_map =  {
            'celsius':      {   
                'symbol':   '°C',
                'aliases':  [
                    'celsius',
                    'Celsius',
                    'C',
                    'c' 
                ]   
            },  
            'fahrenheit':   {   
                'symbol':   '°F',
                'aliases':  [
                    'fahrenheit',
                    'Fahrenheit',
                    'F',
                    'f' 
                ]   
            }   
        }   
        for unit, details in unit_map.iteritems():
            if units in details['aliases']:
                return details['symbol']

    @abc.abstractmethod
    def publish_status(self, target, temp, heater_percent, cooler_percent):
        """
        Publish braubuddy status

        :param target: Target temperature.
        :type target: :class:`float`
        :param temp: Current temperature.
        :type temp: :class:`float`
        :param heater_percent: Current heater power level as percentage.
        :type heater_percent: :class:`float`
        :param cooler_percent: Current cooler power level as percentage.
        :type coolerer_percent: :class:`float`
        """
