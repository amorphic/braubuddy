"""
Braubuddy GraphiteService unit tests
"""

from mock import patch, MagicMock
from braubuddy.tests import BraubuddyTestCase
from braubuddy.output import graphiteservice


class TextFileOutput(BraubuddyTestCase):

    @patch('braubuddy.output.graphiteservice.graphitesend.init')
    def test_graphitesend_initialised(self, mk_graphitesend_init):
        """Graphitesend is initialised on GraphiteServiceOutput init."""

        output = graphiteservice.GraphiteServiceOutput(
            units='celsius', host='testhost.example.com', port=2003,
            prefix='testprefix')
        mk_graphitesend_init.assert_called_with(
            graphite_server='testhost.example.com', graphite_port=2003,
            prefix='testprefix', system_name='')

    @patch('braubuddy.output.graphiteservice.graphitesend.init')
    def test_publish_metrics(self, mk_graphitesend_init):

        output = graphiteservice.GraphiteServiceOutput(
            units='celsius', host='testhost.example.com', port=2003,
            prefix='testprefix')
        output._service = MagicMock()
        output.publish_status(26, 20, 0, 100)
        output._service.send_dict.assert_called_with({
            'target_temp':      26,
            'actual_temp':      20,
            'heater_percent':   0,
            'cooler_percent':   100,
        })
