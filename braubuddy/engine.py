class Engine(object):
    """
    Braubuddy Engine.
    """

    def __init__(self, envcontroller, thermometer, thermostat, outputs):

        self.envcontroller = envcontroller
        self.thermometer = thermometer
        self.thermostat = thermostat
        self.outputs = outputs

    def cycle(self):
        """
        Perform full thermostat cycle and return state.
        """

        # Environment Input
        current_heat, current_cool = self.envcontroller.get_power_levels()
        current_temp = self.thermometer.get_temperature()
        required_heat, required_cool = self.thermostat.get_required_state(
            current_temp, current_heat, current_cool)

        # Set Power Levels
        self.envcontroller.set_heater_level(required_heat)
        self.envcontroller.set_cooler_level(required_cool)

        # Output
        # Should work out a way of doing this outside the engine
        for name, output in self.outputs.iteritems():
            output.publish_status(current_temp, current_heat, current_cool)

        return (current_temp, current_heat, current_cool)
