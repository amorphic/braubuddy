import time
from cherrypy import log
from braubuddy.output import IOutput


class ListMemoryOutput(IOutput):
    """
    Output to a list in memory.

    This is a special output used internally by the Braubuddy engine to store
    metrics for the dashboard and api. It could also be used by a thermostat
    if it required access to past data.

    :param units: Temperature units to output. Use 'celsius' or
        'fahrenheit'.
    :type units: :class:`str`
    :param datapoint_limit: Maximum number of datapoints to store.
    :type datapoint_limit: :class:`int` (0 for unlimited)
    """

    def __init__(self, units='celsius', datapoint_limit=44640):

        self._datapoints = []
        self._datapoint_limit = datapoint_limit
        super(ListMemoryOutput, self).__init__(units)

    def get_datapoints(self, since=None, before=None, limit=None):

        results = self._datapoints
        if since:
            results = [x for x in results if x[4] >= since]
        if before:
            results = [x for x in results if x[4] <= before]
        if limit:
            results = results[-limit:]
        return results

    def publish_status(self, target, temp, heater_percent, cooler_percent):

        # Get timestamp in epoch seconds
        timestamp = int(time.time())
        # Append new status
        status = [target, temp, heater_percent, cooler_percent, timestamp]
        self._datapoints.append(status)
        # Drop datapoints if limit exceeded
        if self._datapoint_limit != 0:
            while len(self._datapoints) > self._datapoint_limit:
                # Discard oldest status datapoint
                log(('Datapoint limit exceeded - dropping earliest datapoint: '
                    '{0!r}').format(self._datapoints[0]))
                self._datapoints.pop(0)
