import os
from datetime import datetime
from xdg import BaseDirectory
from cherrypy import log
import twitter
from braubuddy.output import IOutput
from braubuddy.output import OutputError

APP = 'braubuddy'
TCK = 'p8F5vsNsIsacKuswRwhAfWeoa'
TCS = 'lOL3A2h5pVmBbWfsIsyZpTDa56HeEYFrqgo6OYdEqsyNMxQhI5'

CREDS_FILENAME = 'twitter'
CREDS_PATH = os.path.join(BaseDirectory.xdg_config_home, 'braubuddy')
CREDS_FILE = os.path.join(CREDS_PATH, CREDS_FILENAME)


class TwitterAPIOutput(IOutput):
    """
    Output to the `Twitter <http://www.twitter.com>`_ API.

    .. note::

        When first run this output will attempt to authorise Braubuddy to
        publish to the user's Twitter account. The resulting credentials are
        then retained for future use.

    :param units: Temperature units to output. Use 'celsius' or
        'fahrenheit'.
    :type units: :class:`str`
    :param frequency: Minimum seconds between tweets.
    :type frequency: :class:`int`
    :param message: A template representing the message to be sent to
        Twitter. May include these variables for substitution:

            * temp (actual temperature)
            * target (target temperature)
            * units (temperature units)
            * heat (heater level)
            * cool (cooler level)
    :type message: :class:`str`
    """

    def __init__(self, units='celsius', frequency=1440,
                 message='Environment Status: Temp {temp}{units} | Target '
                         '{target}{units} | Heat {heat}% | Cool {cool}% '
                         '#braubuddy http://braubuddy.org'):

        self._frequency = frequency
        self._message = message
        self._api = self._get_credentials(CREDS_FILE)
        self._last_published = datetime.now()
        super(TwitterAPIOutput, self).__init__(units)

    def _get_credentials(self, creds_file):
        """
        Get Twitter credentials from file if one exists. Otherwise request
        credentials via oauth.
        """

        if not os.path.exists(creds_file):
            print 'Authorising with Twitter...'
            try:
                twitter.oauth_dance(APP, TCK, TCS, creds_file)
            except twitter.TwitterHTTPError as err:
                raise OutputError(err)
        oauth_token, oauth_secret = twitter.read_token_file(creds_file)
        return twitter.Twitter(
            auth=twitter.OAuth(oauth_token, oauth_secret, TCK, TCS))

    def publish_status(self, target, temp, heater_percent, cooler_percent):

        if (datetime.now() - self._last_published).seconds < self._frequency:
            # Don't Tweet until the defined frequency has passed.
            return

        message = self._message.format(units=self.units, temp=temp,
                                       target=target, heat=heater_percent,
                                       cool=cooler_percent)
        if len(message) > 140:
            log.error('TwitterAPIOutput message exceeds 140 '
                      'characters: {0}'.format(message))
        try:
            self._api.statuses.update(status=message)
            self._last_published = datetime.now()
        except Exception as err:
            raise OutputError(
                'Error publishing to Twitter API: {0}'.format(err))
