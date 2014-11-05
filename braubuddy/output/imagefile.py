import time
from datetime import datetime
from os.path import expanduser
import pygal
from braubuddy.output import IOutput
from braubuddy.output import OutputError


FORMATS = {
    'svg': 'render_to_file',
    'png': 'render_to_png',
}


class ImageFileOutput(IOutput):
    """
    Output chart to an image file.

    .. note::
        Heating/cooling as bars with values on 2nd y axis are pending support
        for mixed bar/line graphs in :mod:`pygal`.

    :param units: Temperature units to output. Use 'celsius' or
        'fahrenheit'.
    :type units: :class:`str`
    :param image_path: Path to image file.
    :type image_path: :class:`str`
    :param image_format: Image format ('png' or 'svg').
    :type image_format: :class:`str`
    :param chart_title: Chart title.
    :type chart_title: :class:`str`
    :param chart_mins: Minutes of metric history to chart.
    :type chart_mins: :class:`int`
    :param x_label_mins: Minutes between timestamp labels on x axis.
    :type x_label_mins: :class:`int`
    """

    def __init__(self, units='celsius', out_file='braubuddy.png',
                 out_format='png', chart_title='Braubuddy', chart_mins=10080,
                 x_label_mins=60):
        if out_format not in FORMATS.keys():
            raise OutputError('ImageFileOutput format must be in {0}'.format(
                FORMATS.keys()))
        self._outputter = FORMATS[out_format]
        self._out_file = expanduser(out_file)
        self._past_seconds = chart_mins * 60
        self._x_label_seconds = x_label_mins * 60
        self._datapoints = []

        # Chart config. Many of these values are hard coded to sensible
        # defaults to avoid overwhelming the user with kwargs.
        self._chart_config = pygal.Config()
        self._chart_config.title = chart_title
        self._chart_config.show_dots = False
        self._chart_config.show_minor_x_labels = False
        self._chart_config.x_label_rotation = 20
        self._chart_config.y_label_rotation = 20
        self._chart_config.y_title = 'Temperature'
        self._chart_config.label_font_size = 10
        self._chart_config.legend_font_size = 10
        self._chart_config.tooltip_font_size = 10
        self._chart_config.tooltip_border_radius = 10
        self._chart_config.interpolate = 'cubic'
        self._chart_config.print_values = False

        super(ImageFileOutput, self).__init__(units)

    def publish_status(self, target, temp, heater_percent, cooler_percent):

        # Get timestamp in epoch seconds
        timestamp = int(time.time())
        # Append new status
        status = [target, temp, heater_percent, cooler_percent, timestamp]
        self._datapoints.append(status)
        # Drop datapoints older than required for chart
        earliest = timestamp - self._past_seconds
        self._datapoints = [d for d in self._datapoints
                            if d[4] >= earliest]

        # Divine polling frequency using the difference between timestamps of
        # the most recent 2 datapoints. Use this to set an appropriate x label
        # interval.
        if len(self._datapoints) >= 2:
            freq_seconds = self._datapoints[-1][4] - self._datapoints[-2][4]
            if freq_seconds > 0:
                self._chart_config.x_labels_major_every = (
                    self._x_label_seconds / freq_seconds)

        # Draw chart
        chart = pygal.Line(self._chart_config)
        chart.x_labels = [
            datetime.fromtimestamp(d[4]).strftime('%b-%d %H:%M:%S')
            for d in self._datapoints]
        chart.add('Target', [d[0] for d in self._datapoints])
        chart.add('Actual', [d[1] for d in self._datapoints])
        # TODO: Add heating and cooling as bars once pygal supports bars and
        # lines on a single chart.
        #chart.add('Heating', [d[2] for d in self._datapoints], secondary=True)
        #chart.add('Cooling', [d[3] for d in self._datapoints], secondary=True)
        try:
            getattr(chart, self._outputter)(filename=self._out_file)
        except IOError as err:
            raise OutputError(err)
