from braubuddy.envcontroller import IEnvController 


class DummyEnvController(IEnvController):
    """
    A dummy EnvController. Use for testing.
    """

    def __init__(self): 

        self._heater_percent = 0
        self._cooler_percent = 0

    def set_heater_level(self, percent):

        self._heater_percent = percent

    def set_cooler_level(self, percent):

        self._cooler_percent = percent

    def get_power_levels(self):

        return (self._heater_percent, self._cooler_percent)
