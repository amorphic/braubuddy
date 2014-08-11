.. _configuration:

Configuration
=============

Config File
-----------

About deploying conifg, XDG etc.

Config Parameters
-----------------

+-------------+-------------------+--------------+--------------------------------------+------------------------------+
|Section      |Parameter          |Type          |Default                               |Descrption                    |
+=============+===================+==============+======================================+==============================+
|**global**   |environment        |:class:`str`  |``'production'``                      |Cherrypy environment.         |
|             |                   |              |                                      |``'development'`` or          |
|             |                   |              |                                      |``'production'``.             |
|             +-------------------+--------------+--------------------------------------+------------------------------+
|             |server.socket_host |:class:`str`  |``'0.0.0.0'``                         |Server IP Address.            |
|             +-------------------+--------------+--------------------------------------+------------------------------+
|             |server.socket_port |:class:`int`  |``8080``                              |Server Port.                  |
|             +-------------------+--------------+--------------------------------------+------------------------------+
|             |log.access_file    |:class:`str`  |``’/var/log/braubuddy_access.log’``   |Access log location.          |
|             |                   |              |                                      |*Access logging disabled if   |
|             |                   |              |                                      |undefined*.                   |
|             +-------------------+--------------+--------------------------------------+------------------------------+
|             |log.error_file     |:class:`str`  |``’/var/log/braubuddy_error.log’``    |Error log location.           |
|             |                   |              |                                      |*Error logging disabled if    |
|             |                   |              |                                      |undefined*.                   |
|             +-------------------+--------------+--------------------------------------+------------------------------+
|             |log.screen         |:class:`int`  |``True``                              |Log to screen.                |
|             +-------------------+--------------+--------------------------------------+------------------------------+
|             |units              |:class:`int`  |``'celsius'``                         |Temperature units.            |
|             |                   |              |                                      |``'celsius'`` or              |
|             |                   |              |                                      |``'fahrenheit'``.             |
|             +-------------------+--------------+--------------------------------------+------------------------------+
|             |frequency          |:class:`int`  |``60``                                |Engine cycle frequency.       |
|             +-------------------+--------------+--------------------------------------+------------------------------+
|             |retry_count        |:class:`int`  |``3``                                 |Temperature poll retry count. |
|             +-------------------+--------------+--------------------------------------+------------------------------+
|             |retry_delay        |:class:`int`  |``5``                                 |Temperature poll retry delay. |
|             +-------------------+--------------+--------------------------------------+------------------------------+
|             |show_footer        |:class:`bool` |``True``                              |Show web interface footer.    |
+-------------+-------------------+--------------+--------------------------------------+------------------------------+
|*components* |thermometer        ||ithermometer|||thermometer_auto|                    ||thermometer|.                |
|             +-------------------+--------------+--------------------------------------+------------------------------+
|             |envcontroller      ||iecontroller|||econtroller_auto|                    ||envcontroller|.              |
|             +-------------------+--------------+--------------------------------------+------------------------------+
|             |thermostat         ||ithermostat| ||thermostat_auto|                     ||thermostat|.                 |
+-------------+-------------------+--------------+--------------------------------------+------------------------------+
|*outputs*    |\*                 ||ioutput|     |``None``                              | Any number of |outputs|.     |
+-------------+-------------------+--------------+--------------------------------------+------------------------------+

.. |thermometer| replace:: :ref:`thermometer`
.. |ithermometer| replace:: :class:`braubuddy.thermometer.IThermometer`
.. |thermometer_auto| replace:: :class:`braubuddy.thermometer.AutoThermometer`
.. |envcontroller| replace:: :ref:`Environmental Controller <envcontroller>` 
.. |iecontroller| replace:: :class:`braubuddy.envcontoller.IEnvcontroller`
.. |econtroller_auto| replace:: :class:`braubuddy.envcontoller.AutoEnvcontroller`
.. |thermostat| replace:: :ref:`thermostat` 
.. |ithermostat| replace:: :class:`braubuddy.thermostat.IThermostat`
.. |thermostat_auto| replace:: :class:`braubuddy.thermostat.SimpleRangedThermostat`
.. |outputs| replace:: :ref:`outputs <output>` 
.. |ioutput| replace:: :class:`braubuddy.output.IOutput`
