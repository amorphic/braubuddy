"""
Braubuddy ListMemory unit tests
"""

from braubuddy.tests import BraubuddyTestCase
from braubuddy.output import listmemory


class TestListMemory(BraubuddyTestCase):

    def test_published_datapoint_returned(self):
        """Published datapoint is returned."""
        output = listmemory.ListMemoryOutput()
        target = 20
        temp = 22
        heat = 100
        cool = 0
        output.publish_status(target, temp, heat, cool)
        result = output.get_datapoints()[0]
        self.assertEqual(result[0:4], [target, temp, heat, cool])

    def test_published_datapoints_returned(self):
        """Published datapoints are returned."""
        output = listmemory.ListMemoryOutput()
        for i in range(100):
            output.publish_status(20, 22, 100, 0)
        result = output.get_datapoints()
        self.assertEqual(len(result), 100)

    def test_limited_datapoints_returned(self):
        """Limited datapoints are returned."""
        output = listmemory.ListMemoryOutput()
        for i in range(100):
            output.publish_status(20, 22, 100, 0)
        result = output.get_datapoints(limit=10)
        self.assertEqual(len(result), 10)
