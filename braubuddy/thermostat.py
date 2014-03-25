'''
Braubuddy Thermostat.

Need to be able to reset the target temp with a simple temp val
'''

import abc


class IThermostat(object):
    """
    Interface for creating a thermostat for use with :mod:`braudbuddy`.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, units):
        """
        Initialise thermostat.

        :param units: Temperature units in which to work. Use 'celsius'
            or 'fahrenheit'.
        :type unit: :class:`str`
        """

        self._units = units

    @abc.abstractmethod
    def get_required_state(self, temp, heater_percent, cooler_percent):
        """
        Get the required heater + cooler power levels given the current
        temperature and heater + cooler power levels.

        This is the thermostat's brain. Implement a clever and novel algorithm
        here.

        :param temp: Current temperature.
        :type temp: :class:`float`
        :param heater_percent: Current heater power level.
        :type heater_percent: :class:`int` in range(0-100)
        :param cooler: Current cooler power level.
        :type cooler: :class:`int` in range (0-100)
        :returns: Required heater and cooler power levels.
        :rtype: :class:`tuple` of (:class:`int`, :class:`int`)
        """
        pass


class UpperLowerRange(IThermostat):
    """
    A thermostat which uses an 'upper' temperature range to determine when to
    enable/disable cooling and a 'lower' temperature range to determine when to
    enable/disable heating.

    Heating and cooling are both treated as boolean, thus each is either on
    (100 percent) or off (0 percent).

    The use of inner and outer values prevents flapping, (causing the heater or
    cooler to start and stop repeatedly). This is generally undesirable.

    Here is an example cycle against the upper range on a hot day:

        # Heating and cooling are disabled.
        # Temperature is rising, (it's a hot day).
        # Temperature rises above the upper_out threshold: Cooling is enabled.
        # Temperature is dropping.
        # Temperature drops below the upper_out threshold: Cooling remains
            enabled.
        # Temperature drops below the upper_in threshold: Cooling is disabled.
        # Temperature is rising.
        # Temperature rises above the upper_in threshold: Cooling remains
            disabled.
        # Repeat 

    For a desired temperature of 20C, use something like:

        * lower_out = 18.5
        * lower_in = 19.5
        * upper_in = 20.5
        * upper_out = 21.5

    If this seems too hard, use :class:`SimpleTargeted` which attempts to
    choose sensible values for a given target temperature.

    :param lower_out: Temperature at which heating will switch on.
    :type lower_out: :class:`int`
    :param lower_in: Temperature at which heating will switch off.
    :type lower_in: :class:`int`
    :param upper_in: Temperature at which cooling will switch off.
    :type upper_in: :class:`int`
    :param upper_out: Temperature at which cooling will switch on.
    :type upper_out: :class:`int`
    """

    def __init__(self, units, lower_out, lower_in, upper_in, upper_out):

        self._lower_outside = lower_out
        self._lower_inside = lower_in
        self._upper_inside = upper_in
        self._upper_outside = upper_out
        super(UpperLowerRange, self).__init__(units)

    def get_required_state(self, temp, heater_percent, cooler_percent,):

        # By default heater/cooler percents remain the same
        new_heater_percent = heater_percent
        new_cooler_percent = cooler_percent

        if self._lower_inside < temp < self._upper_inside:
            # Temp within acceptible bounds - heater and cooler off
            new_heater_percent = 0
            new_cooler_percent = 0
        elif temp > self._upper_inside:
            # Temp exceeds upper inside threshold
            if temp > self._upper_outside:
                # Temp exceeds upper outside threshold - heater off|cooler on
                new_heater_percent = 0
                new_cooler_percent = 100
        elif temp < self._lower_inside:
            # Temp exceeds lower inside threshold
            if temp < self._lower_outside:
                # Temp exceeds lower outside threshold - heater on|cooler off
                new_heater_percent = 100
                new_cooler_percent = 0

        return new_heater_percent, new_cooler_percent


class SimpleTargeted(UpperLowerRange):
    """
    A simplified :class:`UpperLowerRange` thermostat.

    Automatically calculates ranges based on target temperature and
    step value.

    :param units: Temperature units in which to work. Use 'celsius'
        or 'fahrenheit'
    :type unit: :class:`str`
    :param target: Target temperature.
    :type target: :class:`int`
    :param step: Step used to calculate thresholds relative to target.
    :type step: :class:`int`
    """

    def __init__(self, units, target, step=1):

        super(SimpleTargeted, self).__init__(
            units,
            target - (step * 2),
            target - step,
            target + step,
            target + (step * 2)
        )
