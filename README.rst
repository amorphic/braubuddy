_logo Braubuddy
===============

.. image:: https://travis-ci.org/amorphic/braubuddy.svg?branch=master
  :alt: Braubuddy CI
  :target: https://travis-ci.org/amorphic/braubuddy

.. _logo image:: images/logo/bb_logo_24x24.png
  :alt: Braubuddy web application
  :target: https://github.com/amorphic/braubuddy

*Braubuddy* is an extensible thermostat framework written in Python. Use *Braubuddy* wherever you need precise temperature control:

- Keep tropical fish swimming happily in water that's 26°C 
- Brew the perfect lager by fermenting at 9°C
- Maximise employee output by maintaining an optimum office ambient air temp of 21.5°C

Features
--------

Web Interface
~~~~~~~~~~~~~

Monitor your thermostat from any device with a web browser.

.. image:: /images/screenshots/1.png
  :alt: Braubuddy web application
  :target: https://github.com/amorphic/braubuddy

API
~~~

Consume time-series temperature, heating and cooling metrics `programatically <http://braubuddy.org>`_.

Outputs
~~~~~~~

Output metrics in various file formats or directly to other APIs.

Modular
~~~~~~~

Support for a growing list of thermometers, environmental controllers, thermostat algorithms and outputs.

Extensible
~~~~~~~~~~

`Request support <http://braubuddy.org>` for the components you need. Better still, extend *Braubuddy*'s simple interfaces to create new components and `submit a pull request <http://braubuddy.org>`_!
 
Compatible
~~~~~~~~~~

Tested under Python 2.6, 2.7 and 3.4. 

Getting Started
---------------

Installation
~~~~~~~~~~~~

*Braubuddy* is best enjoyed from within a Python `virtualenv <http://virtualenv.readthedocs.org/en/latest/>`_:
::

    virtualenv ~/braubuddy
    source ~/braubuddy/bin/activate

Production
^^^^^^^^^^

Install the latest production release from `PyPI <https://pypi.python.org/>`_ using `pip <http://www.pip-installer.org/>`_:

::

    pip install braubuddy

Development
^^^^^^^^^^^

Install the latest development release from `Github <https://github.com/amorphic/braubuddy>`_:

::

    git clone https://github.com/amorphic/braubuddy.git
    pip install -e ./braubuddy

Start
~~~~~


``braubuddy``


Configure
~~~~~~~~~

Before starting, copy the example config file to either:

Home config dir:

``cp etc/braubuddy ~/.config/braubuddy/``

System config dir:

``cp etc/braubuddy /etc/xdg/braubuddy/``

The example config file uses a dummy thermometer and environmental
controller. Follow `the docs <http://braubuddy.org>`_ to configure the components that you wish to use. 

Components
----------

Braubuddy is designed to be extensible. t is easy to add support for new
*Thermometers*, *Environmental Controllers*, *Thermostats* and
*Outputs*.

Thermometer
~~~~~~~~~~~

A *thermometer* is a physical device which measures temperature.

Braubuddy includes support for these *thermometers*:

-  Temper USB
-  DCXXXX

Environmental Controller
~~~~~~~~~~~~~~~~~~~~~~~~

An *environmental controller* is a physical device which controls
heating and cooling levels.

Braubuddy includes support for these *envrionmental controllers*:

-  **Tosr0x**

Thermostat
~~~~~~~~~~

A *thermostat* is an algorithm which takes current and target
temperatures as inputs and produces required heating and cooling levels
as outputs.

Braubuddy includes support for these *thermostats*:

- **SimpleRanged** - *uses an 'upper' temperature range to determine when to enable/disable cooling and a 'lower' temperature range to determine when to enable/disable heating.*

Output
~~~~~~

An *output* is a destination for the metrics collected during each
Braubuddy cycle: *temperature*, *heat level*, *cool level*, *date* and
*time*.

Braubuddy inclues support for these *outputs*:

- TextFile
- CSVFile
- JSONFile

API
---

Metrics collected during each Braubuddy cycle are also available via an
API endpoint: ``http://hostname:port/api/``'.

Metrics are presented as a time series in the format:

``[_temperature_, _heat level_, _cool_level, _epoch time_]``

e.g.

::

    [[25.5, 0, 0, 1402990571], [27.25, 0, 100, 1402990631], [28.5, 0, 100, 1402990692], [29.375, 0, 100, 1402990754], [30.0, 0, 100, 1402990815], [30.25, 0, 100, 1402990876], [30.375, 0, 100, 1402990937], [30.5, 0, 100, 1402990999], [30.375, 0, 100, 1402991060], [30.375, 0, 100, 1402991121], [30.5, 0, 100, 1402991182], [30.375, 0, 100, 1402991243], [30.375, 0, 100, 1402991305], [30.75, 0, 100, 1402991366], [30.875, 0, 100, 1402991427], [31.125, 0, 100, 1402991488]]

Contribute
----------

Braubuddy is designed to be extensible.

- Raise issues for Requests (for hardware w/existing python libs)
- Creating plugins is easy. Send a PR!


