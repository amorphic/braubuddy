"""
Braubuddy LibratoAPI unit tests.
"""

from mock import call, patch, MagicMock
from braubuddy.tests import BraubuddyTestCase
from braubuddy.output import libratoapi


@patch('braubuddy.output.libratoapi.librato.connect')
class LibratoAPIOutput(BraubuddyTestCase):

    def test_librato_api_connect(self, mk_libratoapi_connect):
        """Librato API is initialised on LibratoAPIOutput init."""

        output = libratoapi.LibratoAPIOutput(
            units='celsius', username='myusername', token='mytoken',
            source='braubuddy')
        mk_libratoapi_connect.assert_called_with('myusername', 'mytoken')

    def test_init_sets_source(self, mk_libratoapi_connect):
        """Source is initialised on LibratoAPIOutput init."""

        output = libratoapi.LibratoAPIOutput(
            units='celsius', username='myusername', token='mytoken',
            source='braubuddy')
        self.assertEqual(output._source, 'braubuddy')

    def test_publish_metrics(self, mk_libratoapi_connect):

        output = libratoapi.LibratoAPIOutput(
            units='celsius', username='myusername', token='mytoken',
            source='braubuddy')
        mk_queue = MagicMock()
        output._api = MagicMock()
        output._api.new_queue.return_value = mk_queue
        output.publish_status(26, 20, 0, 100)
        self.assertEqual(
            mk_queue.add.mock_calls,
            [
                call('target_temperature', 26, source='braubuddy'),
                call('actual_temperature', 20, source='braubuddy'),
                call('heater_percent', 0, source='braubuddy'),
                call('cooler_percent', 100, source='braubuddy')
            ])
        self.assertTrue(mk_queue.submit.called)
