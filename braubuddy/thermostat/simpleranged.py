from braubuddy.thermostat import IThermostat


class SimpleRangedThermostat(IThermostat):
    """
    A thermostat which uses an 'upper' temperature range to determine when to
    enable/disable cooling and a 'lower' temperature range to determine when to
    enable/disable heating.

    Heating and cooling are both treated as boolean and thus are either on
    (100 percent) or off (0 percent).

    The use of inner and outer values prevents flapping, (causing the heater or
    cooler to start and stop repeatedly). This is generally undesirable.

    This is an example cycle against the upper range on a hot day:

        #. Heating and cooling are disabled.
        #. Temperature is rising, (it's a hot day).
        #. Temperature rises above the upper_out threshold: Cooling is enabled.
        #. Temperature is dropping.
        #. Temperature drops below the upper_out threshold: Cooling remains
            enabled.
        #. Temperature drops below the upper_in threshold: Cooling is disabled.
        #. Temperature is rising.
        #. Temperature rises above the upper_in threshold: Cooling remains
            disabled.
        #. Repeat

    :param lower_out: Units below target at which heating will switch on.
    :type lower_out: :class:`int`
    :param lower_in: Units below target at which heating will switch off.
    :type lower_in: :class:`int`
    :param upper_in: Units above target at which cooling will switch off.
    :type upper_in: :class:`int`
    :param upper_out: Units above target at which cooling will switch on.
    :type upper_out: :class:`int`
    """

    def __init__(self, target, lower_out=2, lower_in=1, upper_in=1,
                 upper_out=2):

        if lower_out <= lower_in:
            raise ValueError('lower_out must be > lower_in.')
        if upper_out <= upper_in:
            raise ValueError('upper_out must be > upper_in.')
        self._lower_outside = target - lower_out
        self._lower_inside = target - lower_in
        self._upper_inside = target + upper_in
        self._upper_outside = target + upper_out
        super(SimpleRangedThermostat, self).__init__(target)

    def get_required_state(self, temp, heater_percent, cooler_percent,
                           units='celsius'):

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
