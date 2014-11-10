"""
Braubuddy DweetAPI unit tests.
"""

from datetime import datetime, timedelta
from mock import patch
from braubuddy.tests import BraubuddyTestCase
from braubuddy.output import OutputError
from braubuddy.output import dweetapi


@patch('braubuddy.output.dweetapi.dweepy')
class DweetAPIOutput(BraubuddyTestCase):

    def test_post_dweet_successful(self, mk_dweepy):
        """Posting a dweet is successful."""

        thing_name = 'test_thing'
        frequency = 10
        test_output = dweetapi.DweetAPIOutput(
            units='celsius', frequency=frequency, thing_name=thing_name)
        test_output._last_published = datetime.now() - timedelta(
            seconds=(frequency + 1))
        mk_dweepy.dweet_for.return_value = {'this': 'succeeded'}
        expected_dweep = {
            'temperature':  26,
            'target':       20,
            'heater':       0,
            'cooler':       100,
        }
        test_output.publish_status(20, 26, 0, 100)
        mk_dweepy.dweet_for.assert_called_with(thing_name, expected_dweep)

    def test_post_dweet_fails_with_exception(self, mk_dweepy):
        """Posting a dweet is unsuccessful."""

        thing_name = 'test_thing'
        frequency = 10
        test_output = dweetapi.DweetAPIOutput(
            units='celsius', frequency=frequency, thing_name=thing_name)
        test_output._last_published = datetime.now() - timedelta(
            seconds=(frequency + 1))
        mk_dweepy.dweet_for.return_value = {'this': 'succeeded'}
        mk_dweepy.dweet_for.side_effect = Exception('Some error')
        with self.assertRaises(OutputError):
            test_output.publish_status(20, 26, 0, 100)

    def test_post_dweet_fails_with_error_msg(self, mk_dweepy):
        """Posting a dweet is successful."""

        thing_name = 'test_thing'
        frequency = 10
        test_output = dweetapi.DweetAPIOutput(
            units='celsius', frequency=frequency, thing_name=thing_name)
        test_output._last_published = datetime.now() - timedelta(
            seconds=(frequency + 1))
        mk_dweepy.dweet_for.return_value = {'this': 'fail'}
        with self.assertRaises(OutputError):
            test_output.publish_status(20, 26, 0, 100)

    def test_post_skipped_within_interval(self, mk_dweepy):
        """Posting is skipped if interval has not yet passed"""

        thing_name = 'test_thing'
        frequency = 10
        test_output = dweetapi.DweetAPIOutput(
            units='celsius', frequency=frequency, thing_name=thing_name)
        test_output._last_published = datetime.now() - timedelta(
            seconds=(frequency - 1))
        test_output.publish_status(20, 26, 0, 100)
        self.assertFalse(mk_dweepy.dweet_for.called)
