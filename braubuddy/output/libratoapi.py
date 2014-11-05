import librato
from braubuddy.output import IOutput
from braubuddy.output import OutputError


class LibratoAPIOutput(IOutput):
    """
    Output to the `Librato <http://metrics.librato.com>`_ API.

    Requires a Librato username and token, both found on the
        `Account Settings page <https://metrics.librato.com/account>`_.

    :param units: Temperature units to output. Use 'celsius' or
        'fahrenheit'.
    :type units: :class:`str`
    :param username: Librato username.
    :type username: :class:`str`
    :param token: Librato token.
    :type token: class:`str`
    :param source: Librato metric source.
    :type source: :class:`str`
    """

    def __init__(self, units='celsius', username='myusername', token='mytoken',
                 source='braubuddy'):

        self._source = source
        self._api = librato.connect(username, token)
        super(LibratoAPIOutput, self).__init__(units)

    def publish_status(self, target, temp, heater_percent, cooler_percent):

        queue = self._api.new_queue()
        queue.add('target_temperature', target, source=self._source)
        queue.add('actual_temperature', temp, source=self._source)
        queue.add('heater_percent', heater_percent, source=self._source)
        queue.add('cooler_percent', cooler_percent, source=self._source)
        try:
            queue.submit()
        except Exception as err:
            raise OutputError(
                'Error publishing to Librato API: {0}'.format(err))
