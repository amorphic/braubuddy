"""
Braubuddy GraphiteAPI unit tests
"""

from mock import patch, MagicMock
from braubuddy.tests import BraubuddyTestCase
from braubuddy.output import graphiteapi


class GraphiteAPIOutput(BraubuddyTestCase):

    @patch('braubuddy.output.graphiteapi.graphitesend.init')
    def test_graphitesend_initialised(self, mk_graphitesend_init):
        """Graphitesend is initialised on GraphiteAPIOutput init."""

        output = graphiteapi.GraphiteAPIOutput(
            units='celsius', host='testhost.example.com', port=2003,
            prefix='testprefix')
        mk_graphitesend_init.assert_called_with(
            graphite_server='testhost.example.com', graphite_port=2003,
            prefix='testprefix', system_name='')

    @patch('braubuddy.output.graphiteapi.graphitesend.init')
    def test_publish_metrics(self, mk_graphitesend_init):

        output = graphiteapi.GraphiteAPIOutput(
            units='celsius', host='testhost.example.com', port=2003,
            prefix='testprefix')
        output._api = MagicMock()
        output.publish_status(26, 20, 0, 100)
        output._api.send_dict.assert_called_with({
            'target_temp':      26,
            'actual_temp':      20,
            'heater_percent':   0,
            'cooler_percent':   100,
        })
