import json
import time
from os.path import expanduser
from cherrypy import log
from braubuddy.output import IOutput
from braubuddy.output import OutputError


class JSONFileOutput(IOutput):
    """
    Output to JSON file.

    :param units: Temperature units to output. Use 'celsius' or
        'fahrenheit'.
    :type units: :class:`str`
    :param out_file: Path to output file.
    :type out_file: :class:`str`
    :param datapoint_limit: Maximum number of datapoints to store.
    :type datapoint_limit: :class:`int` (0 for unlimited)
    """

    def __init__(self, units='celsius', out_file='braubuddy.json',
                 datapoint_limit=44640):

        self._out_file = expanduser(out_file)
        self._datapoint_limit = datapoint_limit
        super(JSONFileOutput, self).__init__(units)

    def publish_status(self, target, temp, heater_percent, cooler_percent):

        # Load status history from JSON
        try:
            with open(self._out_file, 'r') as fh:
                status_history = json.loads(fh.read())
        except (IOError, ValueError):
            # No existing file or invalid JSON so start with no datapoints
            status_history = []
        # Get timestamp in epoch seconds
        timestamp = int(time.time())
        # Create new status
        status = [target, temp, heater_percent, cooler_percent, timestamp]
        # Add new status to previous data
        status_history.append(status)
        # Drop datapoints if limit exceeded
        if self._datapoint_limit != 0:
            while len(status_history) > self._datapoint_limit:
                # Discard oldest status datapoint
                log('Datapoint limit exceeded - dropping earliest datapoint: '
                    '{0!r}'.format(status_history[0]))
                status_history.pop(0)
        # Write status history JSON to file
        new_json = json.dumps(status_history)
        try:
            with open(self._out_file, 'w+') as fh:
                fh.write(new_json)
        except (IOError, ValueError) as err:
            raise OutputError(err)
