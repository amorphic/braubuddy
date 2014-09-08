# -*- coding: utf-8 -*-
from braubuddy.output import TextFileOutput


class CSVFileOutput(TextFileOutput):
    """
    Output to CSV file.

    This is just a shortcut to create a TextFileOutput in CSV format.

    :param units: Temperature units to output. Use 'celsius' or
        'fahrenheit'.
    :type units: :class:`str`
    :param out_file: Path to output file.
    :type out_file: :class:`str`
    :param show_timestamp: Add timestamp to output values, (e.g.
        2014-01-01 06:40 Temperature:40°C).
    :type show_timestamp: :class:`bool`
    :param timetamp_format: A timestamp format parseable by
        :func:`datetime.datetime.strftime`, (e.g. '%Y-%m-%d %H:%M:%S').
    :type timestamp_format: :class:`str`
    """

    def __init__(self, units='celsius', out_file='braubuddy.csv',
                 show_timestamp=True, timestamp_format='%Y-%m-%d %H:%M:%S'):

        super(CSVFileOutput, self).__init__(
            units=units, out_file=out_file, separator=',', show_labels=False,
            show_units=False, show_timestamp=show_timestamp,
            timestamp_format=timestamp_format)
