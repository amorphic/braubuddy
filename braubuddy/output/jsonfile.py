import logging
import json
import time
from braubuddy.output import IOutput

LOGGER = logging.getLogger(__name__)


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

        self._out_file = out_file
        self._datapoint_limit = datapoint_limit
        super(JSONFileOutput, self).__init__(units)

    def publish_status(self, temp, heater_percent, cooler_percent):
        
        # Load status history from JSON
        try:
            with open(self._out_file, 'r') as fh:
                status_history = json.loads(fh.read())
            fh.close()
        except (IOError, ValueError):
            # No existing file or invalid JSON so start with no datapoints
            status_history = {
                'datapoints' : []
            }
        # Check data loaded from JSON contains datapoints
        if 'datapoints' not in status_history.keys():
            raise OutputError(
                "JSON in file {0} does not contain key 'datapoints'".format(
                    self._out_file
                )
            )
        # Get timestamp in epoch seconds
        timestamp = int(time.time())
        # Create new status
        status = [temp, heater_percent, cooler_percent, timestamp]
        # Add new status to previous data
        status_history['datapoints'].append(status)
        # Drop datapoints if limit exceeded
        if self._datapoint_limit != 0:
            while len(status_history['datapoints']) > self._datapoint_limit:
                # Discard oldest status datapoint
                LOGGER.debug(('Datapoint limit exceeded - '
                    'dropping earliest datapoint: {0!r}').format(
                        status_history['datapoints'][0]))
                status_history['datapoints'].pop(0)
        # Write status history JSON to file
        new_json = json.dumps(status_history)
        fh = open(self._out_file, 'w')
        fh.write(new_json)
        fh.close()
