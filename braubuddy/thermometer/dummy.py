import random
from braubuddy import utils
from braubuddy.thermometer import IThermometer


class DummyThermometer(IThermometer):
    """
    A dummy thermometer which generates random temperature readings within
    a defined range. Use for testing.

    :param `lower_bound`: Lower bound of returned temperature range
    :type `lower_bound`: :class:`int`
    :param `upper_bound`: Upper bound of returned temperature range
    :type `upper_bound`: :class:`int`
    """

    def __init__(self, lower_bound=20, upper_bound=30):
        # Set random range bounds
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        super(DummyThermometer, self).__init__()

    def get_temperature(self, units='celsius'):
        # Returns random temperature within defined range
        current_temp = random.randrange(self.lower_bound, self.upper_bound)
        if units == 'fahrenheit':
            current_temp = utils.convert_temp_units(
                current_temp,
                units_from='celsius',
                units_to='fahrenheit'
            )
        return current_temp
