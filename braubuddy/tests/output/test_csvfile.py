# -*- coding: utf-8 -*-
"""
Braubuddy CSVFileOutput unit tests
"""

from tempfile import NamedTemporaryFile
from braubuddy.tests import BraubuddyTestCase
from braubuddy.output import csvfile


class CSVFileOutput(BraubuddyTestCase):

    def setUp(self):
        self.target = 20
        self.temp = 25
        self.heat = 0
        self.cool = 10

    def test_set_units_to_fahrenheit(self):
        """Units are set to fahrenheit."""
        outfile = NamedTemporaryFile()
        output = csvfile.CSVFileOutput(
            units='fahrenheit',
            out_file=outfile.name
        )
        output.publish_status(self.temp, self.target, self.heat, self.cool)
        expected = u'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,25,20,0,10\n'
        self.assertRegexpMatches(outfile.read().decode('UTF-8'), expected)

    def test_set_show_timestamp(self):
        """Timestamps are included in output lines."""
        outfile = NamedTemporaryFile()
        output = csvfile.CSVFileOutput(
            show_timestamp=True,
            out_file=outfile.name
        )
        output.publish_status(self.temp, self.target, self.heat, self.cool)
        expected = u'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,25,20,0,10\n'
        self.assertRegexpMatches(outfile.read().decode('UTF-8'), expected)

    def test_unset_show_timestamp(self):
        """Timestamps are not included in output lines."""
        outfile = NamedTemporaryFile()
        output = csvfile.CSVFileOutput(
            show_timestamp=False,
            out_file=outfile.name
        )
        output.publish_status(self.temp, self.target, self.heat, self.cool)
        expected = u'25,20,0,10\n'
        self.assertRegexpMatches(outfile.read().decode('UTF-8'), expected)

    def test_set_timestamp_format(self):
        """Timestamps are output in specified format."""
        outfile = NamedTemporaryFile()
        output = csvfile.CSVFileOutput(
            show_timestamp=True,
            timestamp_format='%D %H:%M',
            out_file=outfile.name
        )
        output.publish_status(self.temp, self.target, self.heat, self.cool)
        expected = u'\d\d/\d\d/\d\d \d\d:\d\d,25,20,0,10'
        self.assertRegexpMatches(outfile.read().decode('UTF-8'), expected)
