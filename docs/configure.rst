.. _configuration:

Configuration
=============

The *Braubuddy* configuration file allows target temperature, temperature units, outputs and various other parameters to be defined.

File
----

*Braubuddy* conforms to a subset of the `XDG Base Directory Specification`_ for configuration file locations:

    1. ``/etc/xdg/braubuddy`` - Configuratin file  to be used system-wide.
    2. ``/home/<user>/.config/braubuddy`` - Configuration file for the current user. Over-rides the system configuration file if present.

If not present on startup, a default configuration file is deployed to ``~/.config/braubuddy/``.
 
Parameters
----------

+-------------+-------------------+---------------+--------------------------------------+------------------------------+
|Section      |Parameter          |Type           |Default                               |Descrption                    |
+=============+===================+===============+======================================+==============================+
|**global**   |environment        |:class:`str`   |``'production'``                      |Cherrypy environment.         |
|             |                   |               |                                      |``'development'`` or          |
|             |                   |               |                                      |``'production'``.             |
|             +-------------------+---------------+--------------------------------------+------------------------------+
|             |server.socket_host |:class:`str`   |``'0.0.0.0'``                         |Server IP Address.            |
|             +-------------------+---------------+--------------------------------------+------------------------------+
|             |server.socket_port |:class:`int`   |``8080``                              |Server Port.                  |
|             +-------------------+---------------+--------------------------------------+------------------------------+
|             |log.access_file    |:class:`str`   |``’/var/log/braubuddy_access.log’``   |Access log location.          |
|             |                   |               |                                      |*Access logging disabled if   |
|             |                   |               |                                      |undefined*.                   |
|             +-------------------+---------------+--------------------------------------+------------------------------+
|             |log.error_file     |:class:`str`   |``’/var/log/braubuddy_error.log’``    |Error log location.           |
|             |                   |               |                                      |*Error logging disabled if    |
|             |                   |               |                                      |undefined*.                   |
|             +-------------------+---------------+--------------------------------------+------------------------------+
|             |log.screen         |:class:`int`   |``True``                              |Log to screen.                |
|             +-------------------+---------------+--------------------------------------+------------------------------+
|             |units              |:class:`int`   |``'celsius'``                         |Temperature units.            |
|             |                   |               |                                      |``'celsius'`` or              |
|             |                   |               |                                      |``'fahrenheit'``.             |
|             +-------------------+---------------+--------------------------------------+------------------------------+
|             |frequency          |:class:`int`   |``60``                                |Engine cycle frequency.       |
|             +-------------------+---------------+--------------------------------------+------------------------------+
|             |retry_count        |:class:`int`   |``3``                                 |Temperature poll retry count. |
|             +-------------------+---------------+--------------------------------------+------------------------------+
|             |retry_delay        |:class:`int`   |``5``                                 |Temperature poll retry delay. |
|             +-------------------+---------------+--------------------------------------+------------------------------+
|             |show_footer        |:class:`bool`  |``True``                              |Show web interface footer.    |
+-------------+-------------------+---------------+--------------------------------------+------------------------------+
|*components* |thermometer        ||ithermometer| ||thermometer_auto|                    ||thermometer|.                |
|             +-------------------+---------------+--------------------------------------+------------------------------+
|             |envcontroller      ||iecontroller| ||econtroller_auto|                    ||envcontroller|.              |
|             +-------------------+---------------+--------------------------------------+------------------------------+
|             |thermostat         ||ithermostat|  ||thermostat_simpleranged|             ||thermostat|.                 |
+-------------+-------------------+---------------+--------------------------------------+------------------------------+
|*outputs*    |\*                 ||ioutput|      |``None``                              | Any number of |outputs|.     |
+-------------+-------------------+---------------+--------------------------------------+------------------------------+

.. |thermometer| replace:: :ref:`thermometer`
.. |ithermometer| replace:: :class:`braubuddy.thermometer.IThermometer`
.. |thermometer_auto| replace:: :ref:`AutoThermometer`
.. |envcontroller| replace:: :ref:`Environmental Controller <envcontroller>` 
.. |iecontroller| replace:: :class:`braubuddy.envcontoller.IEnvcontroller`
.. |econtroller_auto| replace:: :ref:`AutoEnvController`
.. |thermostat| replace:: :ref:`thermostat` 
.. |ithermostat| replace:: :class:`braubuddy.thermostat.IThermostat`
.. |thermostat_simpleranged| replace:: :ref:`SimpleRangedThermostat`
.. |outputs| replace:: :ref:`outputs <output>` 
.. |ioutput| replace:: :class:`braubuddy.output.IOutput`
.. _XDG Base Directory Specification: http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
