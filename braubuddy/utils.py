"""
Braubuddy utility functions.
"""

def abbreviate_temp_units(units):
    """
    Abbreviate temperature full name to single letter.

    :param units: Temperature units to abbreviate.
    :type units: :class:`string`
    """
    conversion_map = {
        'celsius':      'C',
        'Celsius':      'C',
        'Farenheit':    'F',
        'farenheit':    'F',
    }
    if units not in conversion_map.keys():
        raise KeyError('Unable to abbreviate {0}. Unknown unit.'.format(units))
    return conversion_map[units]
