"""
Braubuddy TwitterAPI unit tests
"""

import os
import tempfile
import shutil
from datetime import datetime, timedelta
import xdg
from mock import patch, MagicMock
from braubuddy.tests import BraubuddyTestCase
from braubuddy.output import OutputError
from braubuddy.output import twitterapi


class TwitterAPIOutputAuth(BraubuddyTestCase):

    @patch('braubuddy.output.twitterapi.TwitterAPIOutput._get_credentials')
    def test_create_get_credentials_(self, mk_get_create_creds):
        """Credentials are loaded from expected location on instantiation."""
        creds_file = os.path.join(
            os.path.join(xdg.BaseDirectory.xdg_config_home, twitterapi.APP),
            twitterapi.CREDS_FILE)
        tapi = twitterapi.TwitterAPIOutput()
        mk_get_create_creds.assert_called_once_with(creds_file)

    @patch('braubuddy.output.twitterapi.twitter.OAuth')
    def test_auth_with_creds_file(self, mk_OAuth):
        """An existing credentials file is used."""
        fake_token = '0123456789'
        fake_secret = 'abcdefghij'
        fake_creds_file = tempfile.mkstemp()
        os.write(
            fake_creds_file[0], '{0}\n{1}\n'.format(fake_token, fake_secret))
        mk_creds = fake_creds_file[1]
        with patch('braubuddy.output.twitterapi.CREDS_FILE', new=mk_creds):
            test_output = twitterapi.TwitterAPIOutput()
            mk_OAuth.assert_called_once_with(
                fake_token,
                fake_secret,
                twitterapi.TCK,
                twitterapi.TCS)
        os.close(fake_creds_file[0])
        os.remove(fake_creds_file[1])

    @patch('braubuddy.output.twitterapi.twitter')
    def test_auth_without_creds_file(self, mk_twitter):
        """A new credentials file is created."""
        fake_token = '0123456789'
        fake_secret = 'abcdefghij'
        fake_creds_dir = tempfile.mkdtemp()
        fake_creds_file = os.path.join(
            fake_creds_dir, twitterapi.CREDS_FILENAME)
        mk_twitter.read_token_file.return_value = (fake_token, fake_secret)
        with patch('braubuddy.output.twitterapi.CREDS_FILE',
                   new=fake_creds_file):
            test_output = twitterapi.TwitterAPIOutput()
            mk_twitter.oauth_dance.assert_called_once_with(
                twitterapi.APP,
                twitterapi.TCK,
                twitterapi.TCS,
                fake_creds_file)
        shutil.rmtree(fake_creds_dir)


class TwitterAPIOutputPost(BraubuddyTestCase):

    @patch('braubuddy.output.twitterapi.twitter.OAuth')
    def setUp(self, mk_OAuth):
        # Create a fake output.
        fake_token = '0123456789'
        fake_secret = 'abcdefghij'
        fake_creds_file = tempfile.mkstemp()
        os.write(
            fake_creds_file[0], '{0}\n{1}\n'.format(fake_token, fake_secret))
        mk_creds = fake_creds_file[1]
        with patch('braubuddy.output.twitterapi.CREDS_FILE', new=mk_creds):
            self.test_output = twitterapi.TwitterAPIOutput()
        self.test_output._api = MagicMock()
        os.close(fake_creds_file[0])
        os.remove(fake_creds_file[1])

    def test_post_tweet_unsuccessful(self):
        """Unsucessful post raises an OutputError."""
        self.test_output._last_published = datetime.now() - timedelta(
            seconds=(self.test_output._frequency + 1))
        self.test_output._api.statuses.update.side_effect = Exception(
            'Some error')
        with self.assertRaises(OutputError):
            self.test_output.publish_status(20, 26, 0, 100)

    def test_post_tweet_successful(self):
        """Posting a tweet is sucessful."""
        self.test_output._last_published = datetime.now() - timedelta(
            seconds=(self.test_output._frequency + 1))
        units = self.test_output.units
        temp = 26
        target = 20
        heat = 0
        cool = 100
        expected_message = self.test_output._message.format(
            units=units, temp=temp, target=target, heat=heat, cool=cool)
        self.test_output.publish_status(20, 26, 0, 100)
        self.test_output._api.statuses.update.assert_called_once_with(
            status=expected_message)

    def test_post_skipped_within_interval(self):
        """Posting is skipped if interval has not yet passed"""
        self.test_output._last_published = datetime.now() - timedelta(
            seconds=(self.test_output._frequency - 1))
        self.test_output.publish_status(20, 26, 0, 100)
        self.assertFalse(
            self.test_output._api.statuses.update.called)
