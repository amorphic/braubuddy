# -*- coding: utf-8 -*-
"""
Braubuddy Output
"""

import os
import abc
import logging
import json
import time
from datetime import datetime

LOGGER = logging.getLogger(__name__)

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
            self.units = map_temp_units_to_symbol(new_units)
        except:
            raise OutputError('Unrecognised units: {0}'.format(units))

    @abc.abstractmethod
    def publish_status(self, temp, heater_percent, cooler_percent):
        """
        Publish braubuddy status

        :param temp: Current temperature.
        :type temp: :class:`float`
        :param heater_percent: Current heater power level as percentage.
        :type heater_percent: :class:`float`
        :param cooler_percent: Current cooler power level as percentage.
        :type coolerer_percent: :class:`float`
        """

class TextFileOutput(IOutput):
    """
    Output to text file.

    :param units: Temperature units to output. Use 'celsius' or
        'fahrenheit'.
    :type units: :class:`str`
    :param out_file: Path to output file.
    :type out_file: :class:`str`
    :param separator: Separator between line output values.
    :type separator: :class:`str`
    :param show_labels: Add label to output values, (e.g. 'Temperature:40').
    :type show_labels: :class`bool`
    :param show_units: Add units to output values, (e.g. '40°C').
    :type show_units: :class:`bool`
    :param show_timestamp Add timestamp to output values, (e.g.
        2014-01-01 06:40 Temperature:40°C).
    :param timetamp_format: A timestamp format parseable by
        :func:`datetime.datetime.strftime`, (e.g. '%Y-%m-%d %H:%M:%S').
    :type timestamp_format: :class:`str`
    """

    def __init__(self, units='celsius', out_file='braubuddy.log',
            separator=' ', show_labels=False, show_units=True,
            show_timestamp=True, timestamp_format='%Y-%m-%d %H:%M:%S'):

        self._out_file = out_file
        self._separator = separator
        self._show_labels = show_labels
        self._show_units = show_units
        self._show_timestamp = show_timestamp
        self._timestamp_format = timestamp_format
        super(TextFileOutput, self).__init__(units)

    def publish_status(self, temp, heater_percent, cooler_percent):
        
        temp_str = temp
        heater_str = heater_percent
        cooler_str = cooler_percent
        # Add units if required
        if self._show_units:
            temp_str = '{0}{1}'.format(temp_str, self.units)
            heater_str = '{0}%'.format(heater_str)
            cooler_str = '{0}%'.format(cooler_str)
        # Add labels if required
        if self._show_labels:
            temp_str = 'Temperature:{0}'.format(temp_str)
            heater_str = 'Heater:{0}'.format(heater_str)
            cooler_str = 'Cooler:{0}'.format(cooler_str)
        # Generate output line
        line = '{1}{0}{2}{0}{3}\n'.format(
            self._separator,
            temp_str,
            heater_str,
            cooler_str
        )
        # Add timestamp if required
        if self._show_timestamp:
            timestamp = datetime.now().strftime(self._timestamp_format)
            line = '{0}{1}{2}'.format(timestamp, self._separator, line)
        try:
            fh = open(self._out_file, 'a')
            fh.write(line)
            fh.close()
        except IOError, err:
            raise OutputError(err)

class CSVFileOutput(TextFileOutput):
    """
    Output to CSV file.

    :param units: Temperature units to output. Use 'celsius' or
        'fahrenheit'.
    :type units: :class:`str`
    :param out_file: Path to output file.
    :type out_file: :class:`str`
    :param show_timestamp Add timestamp to output values, (e.g.
        2014-01-01 06:40 Temperature:40°C).
    :param timetamp_format: A timestamp format parseable by
        :func:`datetime.datetime.strftime`, (e.g. '%Y-%m-%d %H:%M:%S').
    """

    def __init__(self, units='celsius', out_file='braubuddy.csv',
        show_timestamp=True, timestamp_format='%Y-%m-%d %H:%M:%S'):

        separator = ',' 
        super(CSVFileOutput, self).__init__(units, out_file=out_file,
            separator=separator, show_timestamp=show_timestamp,
            timestamp_format=timestamp_format)

class ListMemoryOutput(IOutput):
    """
    Output to a list in memory

    :param units: Temperature units to output. Use 'celsius' or
        'fahrenheit'.
    :type units: :class:`str`
    :param datapoint_limit: Maximum number of datapoints to store.
    :type datapoint_limit: :class:`int` (0 for unlimited)
    """

    def __init__(self, units='celsius', datapoint_limit=44640):
        
        self._datapoints = []
        self._datapoint_limit = datapoint_limit
        super(ListMemoryOutput, self).__init__(units)

    def get_datapoints(self, since=None, before=None, limit=None):
        
        results = self._datapoints
        if since:
            results = [x for x in results if x[3] >= since]
        if before:
            results = [x for x in results if x[3] <= before]
        if limit:
            results = results[-limit:]
        return results 

    def publish_status(self, temp, heater_percent, cooler_percent):
        
        # Get timestamp in epoch seconds
        timestamp = int(time.time())
        # Append new status
        status = [temp, heater_percent, cooler_percent, timestamp]
        self._datapoints.append(status)
        # Drop datapoints if limit exceeded
        if self._datapoint_limit != 0:
            while len(self._datapoints) > self._datapoint_limit:
                # Discard oldest status datapoint
                LOGGER.debug(
                    (
                        'Datapoint limit exceeded - '
                        'dropping earliest datapoint: {0!r}'
                    ).format(self._datapoints[0]
                ))
                self._datapoints.pop(0)
        

class JSONFileOutput(IOutput):
    """
    Output to JSON file.

    :param units: Temperature units to output. Use 'celsius' or
        'fahrenheit'.
    :type units: :class:`str`
    :param out_file: Path to output file.
    :type out_file: :class:`str`
    :param datapoint_limit: Maximum number of datapoints to store.
    :type datapoint_limit: :class:`int` (0 for unlimited)
    """

    def __init__(self, units='celsius', out_file='braubuddy.json',
        datapoint_limit=44640):

        self._out_file = out_file
        self._datapoint_limit = datapoint_limit
        super(JSONFileOutput, self).__init__(units)

    def publish_status(self, temp, heater_percent, cooler_percent):
        
        # Load status history from JSON
        try:
            with open(self._out_file, 'r') as fh:
                status_history = json.loads(fh.read())
            fh.close()
        except (IOError, ValueError):
            # No existing file or invalid JSON so start with no datapoints
            status_history = {
                'datapoints' : []
            }
        # Check data loaded from JSON contains datapoints
        if 'datapoints' not in status_history.keys():
            raise OutputError(
                "JSON in file {0} does not contain key 'datapoints'".format(
                    self._out_file
                )
            )
        # Get timestamp in epoch seconds
        timestamp = int(time.time())
        # Create new status
        status = [temp, heater_percent, cooler_percent, timestamp]
        # Add new status to previous data
        status_history['datapoints'].append(status)
        # Drop datapoints if limit exceeded
        if self._datapoint_limit != 0:
            while len(status_history['datapoints']) > self._datapoint_limit:
                # Discard oldest status datapoint
                LOGGER.debug(('Datapoint limit exceeded - '
                    'dropping earliest datapoint: {0!r}').format(
                        status_history['datapoints'][0]))
                status_history['datapoints'].pop(0)
        # Write status history JSON to file
        new_json = json.dumps(status_history)
        fh = open(self._out_file, 'w')
        fh.write(new_json)
        fh.close()
