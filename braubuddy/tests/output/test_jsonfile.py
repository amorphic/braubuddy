"""
Braubuddy JSONFileOutput unit tests
"""

import json
from random import randrange
from time import time
from tempfile import NamedTemporaryFile
from braubuddy.tests import BraubuddyTestCase
from braubuddy.output import jsonfile


class JSONFileOutput(BraubuddyTestCase):

    def test_publish_metric(self):
        """A single metric is published."""
        outfile = NamedTemporaryFile()
        output = jsonfile.JSONFileOutput(
            units='fahrenheit',
            out_file=outfile.name
        )
        t = int(time())
        output.publish_status(25, 20, 100, 0)
        self.assertEquals(
            json.load(outfile)[0],
            [25, 20, 100, 0, t]
        )

    def test_publish_metrics(self):
        """Multiple metrics are published."""
        outfile = NamedTemporaryFile()
        output = jsonfile.JSONFileOutput(
            units='fahrenheit',
            out_file=outfile.name
        )
        expected = []
        # publish metrics
        for d in range(20):
            target = 20
            temp = randrange(15, 25)
            if temp > target:
                heat = 0
                cool = 100
            elif temp < target:
                heat = 100
                cool = 0
            else:
                heat = 0
                cool = 0
            now = int(time())
            output.publish_status(target, temp, heat, cool)
            expected.append([target, temp, heat, cool, now])
        self.assertEquals(
            json.load(outfile),
            expected
        )
