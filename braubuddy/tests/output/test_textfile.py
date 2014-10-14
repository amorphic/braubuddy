# -*- coding: utf-8 -*-
"""
Braubuddy TextOutput unit tests
"""

from tempfile import NamedTemporaryFile
from braubuddy.tests import BraubuddyTestCase
from braubuddy.output import textfile


class TextFileOutput(BraubuddyTestCase):

    def setUp(self):
        self.target = 20
        self.temp = 25
        self.heat = 0
        self.cool = 10

    def test_set_units_to_fahrenheit(self):
        """Units are set to fahrenheit."""
        outfile = NamedTemporaryFile()
        output = textfile.TextFileOutput(
            units='fahrenheit',
            out_file=outfile.name
        )
        output.publish_status(self.temp, self.target, self.heat, self.cool)
        expected = u'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d 25°F 20°F 0% 10%\n'
        self.assertRegexpMatches(outfile.read().decode('UTF-8'), expected)

    def test_set_separator(self):
        """Separators are included between values in output lines."""
        outfile = NamedTemporaryFile()
        output = textfile.TextFileOutput(
            units='fahrenheit',
            separator=',',
            out_file=outfile.name
        )
        output.publish_status(self.temp, self.target, self.heat, self.cool)
        expected = u'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,25°F,20°F,0%,10%\n'
        self.assertRegexpMatches(outfile.read().decode('UTF-8'), expected)

    def test_set_show_labels(self):
        """Temperature labels are included in output lines."""
        outfile = NamedTemporaryFile()
        output = textfile.TextFileOutput(
            units='fahrenheit',
            separator=',',
            show_labels=True,
            out_file=outfile.name
        )
        output.publish_status(self.temp, self.target, self.heat, self.cool)
        expected = u'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,Target:25°F,' \
            + u'Temperature:20°F,Heater:0%,Cooler:10%\n'
        self.assertRegexpMatches(outfile.read().decode('UTF-8'), expected)

    def test_unset_show_labels(self):
        """Temperature labels are not included in output lines."""
        outfile = NamedTemporaryFile()
        output = textfile.TextFileOutput(
            units='fahrenheit',
            separator=',',
            show_labels=False,
            out_file=outfile.name
        )
        output.publish_status(self.temp, self.target, self.heat, self.cool)
        expected = u'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,25°F,20°F,0%,10%\n'
        self.assertRegexpMatches(outfile.read().decode('UTF-8'), expected)

    def test_set_show_units(self):
        """Temperature units are included in output lines."""
        outfile = NamedTemporaryFile()
        output = textfile.TextFileOutput(
            units='fahrenheit',
            separator=',',
            show_labels=True,
            show_units=True,
            out_file=outfile.name
        )
        output.publish_status(self.temp, self.target, self.heat, self.cool)
        expected = u'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,Target:25°F,' \
            + u'Temperature:20°F,Heater:0%,Cooler:10%\n'
        self.assertRegexpMatches(outfile.read().decode('UTF-8'), expected)

    def test_unset_show_units(self):
        """Temperature units are not included in output lines."""
        outfile = NamedTemporaryFile()
        output = textfile.TextFileOutput(
            units='fahrenheit',
            separator=',',
            show_labels=True,
            show_units=False,
            out_file=outfile.name
        )
        output.publish_status(self.temp, self.target, self.heat, self.cool)
        expected = u'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,Target:25,' \
            + u'Temperature:20,Heater:0,Cooler:10\n'
        self.assertRegexpMatches(outfile.read().decode('UTF-8'), expected)

    def test_set_show_timestamp(self):
        """Timestamps are included in output lines."""
        outfile = NamedTemporaryFile()
        output = textfile.TextFileOutput(
            units='fahrenheit',
            separator=',',
            show_labels=True,
            show_units=True,
            show_timestamp=True,
            out_file=outfile.name
        )
        output.publish_status(self.temp, self.target, self.heat, self.cool)
        expected = u'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,Target:25°F,' \
            + u'Temperature:20°F,Heater:0%,Cooler:10%\n'
        self.assertRegexpMatches(outfile.read().decode('UTF-8'), expected)

    def test_unset_show_timestamp(self):
        """Timestamps are not included in output lines."""
        outfile = NamedTemporaryFile()
        output = textfile.TextFileOutput(
            units='fahrenheit',
            separator=',',
            show_labels=True,
            show_units=True,
            show_timestamp=False,
            out_file=outfile.name
        )
        output.publish_status(self.temp, self.target, self.heat, self.cool)
        expected = u'Target:25°F,Temperature:20°F,Heater:0%,Cooler:10%\n'
        self.assertRegexpMatches(outfile.read().decode('UTF-8'), expected)

    def test_set_timestamp_format(self):
        """Timestamps are output in specified format."""
        outfile = NamedTemporaryFile()
        output = textfile.TextFileOutput(
            units='fahrenheit',
            separator=',',
            show_labels=True,
            show_units=True,
            show_timestamp=True,
            timestamp_format='%D %H:%M',
            out_file=outfile.name
        )
        output.publish_status(self.temp, self.target, self.heat, self.cool)
        expected = u'\d\d/\d\d/\d\d \d\d:\d\d,Target:25°F,' \
            + u'Temperature:20°F,Heater:0%,Cooler:10%\n'
        self.assertRegexpMatches(outfile.read().decode('UTF-8'), expected)
