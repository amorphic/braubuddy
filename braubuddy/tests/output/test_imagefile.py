"""
Braubuddy ImageFileOutput unit tests
"""

import os
from tempfile import NamedTemporaryFile
from braubuddy.tests import BraubuddyTestCase
from braubuddy.output import imagefile


class ImageFileOutput(BraubuddyTestCase):

    def test_publish_metric(self):
        """A single metric is published."""
        with NamedTemporaryFile() as outfile:
            output = imagefile.ImageFileOutput(
                units='celsius',
                out_file=outfile.name,
                out_format='png',
                chart_title='Braubuddy',
                chart_mins=10080,
                x_label_mins=60)
            output.publish_status(25, 20, 100, 0)
            self.assertTrue(os.path.isfile(outfile.name))
