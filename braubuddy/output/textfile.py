# -*- coding: utf-8 -*-
from datetime import datetime
from os.path import expanduser
from braubuddy.output import IOutput
from braubuddy.output import OutputError


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
    :param show_labels: Add labels to output values, (e.g. 'Temperature:40').
    :type show_labels: :class`bool`
    :param show_units: Add units to output values, (e.g. '40°C').
    :type show_units: :class:`bool`
    :param show_timestamp: Add timestamp to output values, (e.g.
        2014-01-01 06:40 Temperature:40°C).
    :type show_timestamp: :class:`bool`
    :param timetamp_format: A timestamp format parseable by
        :func:`datetime.datetime.strftime`, (e.g. '%Y-%m-%d %H:%M:%S').
    :type timestamp_format: :class:`str`
    """

    def __init__(self, units='celsius', out_file='braubuddy.log',
                 separator=' ', show_labels=False, show_units=True,
                 show_timestamp=True, timestamp_format='%Y-%m-%d %H:%M:%S'):

        self._out_file = expanduser(out_file)
        self._separator = separator
        self._show_labels = show_labels
        self._show_units = show_units
        self._show_timestamp = show_timestamp
        self._timestamp_format = timestamp_format
        super(TextFileOutput, self).__init__(units)

    def publish_status(self, target, temp, heater_percent, cooler_percent):

        target_str = target
        temp_str = temp
        heater_str = heater_percent
        cooler_str = cooler_percent
        # Add units if required
        if self._show_units:
            target_str = '{0}{1}'.format(target_str, self.units)
            temp_str = '{0}{1}'.format(temp_str, self.units)
            heater_str = '{0}%'.format(heater_str)
            cooler_str = '{0}%'.format(cooler_str)
        # Add labels if required
        if self._show_labels:
            target_str = 'Target:{0}'.format(target_str)
            temp_str = 'Temperature:{0}'.format(temp_str)
            heater_str = 'Heater:{0}'.format(heater_str)
            cooler_str = 'Cooler:{0}'.format(cooler_str)
        # Generate output line
        line = '{1}{0}{2}{0}{3}{0}{4}\n'.format(
            self._separator,
            target_str,
            temp_str,
            heater_str,
            cooler_str
        )
        # Add timestamp if required
        if self._show_timestamp:
            timestamp = datetime.now().strftime(self._timestamp_format)
            line = '{0}{1}{2}'.format(timestamp, self._separator, line)
        try:
            fh = open(self._out_file, 'a+')
            fh.write(line)
            fh.close()
        except IOError, err:
            raise OutputError(err)
