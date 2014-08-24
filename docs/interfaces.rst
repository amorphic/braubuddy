Interfaces
==========

.. toctree::
    :maxdepth: 3

*Braubuddy* components are built upon Abstract Base Classes (:mod:`abc`):

.. autosummary::
    braubuddy.thermometer.base
    braubuddy.envcontroller.base
    braubuddy.thermostat.base
    braubuddy.output.base

To add support for a new component simply extend the appropriate ABC. Consult the source of an existing component to get started and don't forget to :ref:`contribute <contribute>` your new component back to the *Braubuddy* project when you're done!

Thermometer
-----------

.. autoclass:: braubuddy.thermometer.base.IThermometer
    :members:
    :undoc-members:
    :noindex:

EnvController
-------------

.. autoclass:: braubuddy.envcontroller.base.IEnvController
    :members:
    :undoc-members:
    :noindex:

Thermostat
----------

.. autoclass:: braubuddy.thermostat.base.IThermostat
    :members:
    :undoc-members:
    :noindex:

Output
------

.. autoclass:: braubuddy.output.base.IOutput
    :members:
    :undoc-members:
    :noindex:
