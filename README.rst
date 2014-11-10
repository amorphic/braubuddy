|logo| Braubuddy
================

|travis| |downloads| |versions| 

*Braubuddy* is a temperature management framework written in Python.

Conceived as a means of monitoring and controlling the fermentation temperature of beer, *Braubuddy* can be used in any situation where visibility and/or control of temperature is critical:

- Keep tropical fish swimming happily in water that's 26°C 
- Brew a perfect lager by fermenting at a constant 9°C
- Maximise employee productivity with an optimum office ambient air temp of 21.5°C

Complete documentation is available at `braubuddy.org <http://braubuddy.org>`_.

Features
--------

Web Interface
^^^^^^^^^^^^^

*Braubuddy*'s web interface facilitates temperature monitoring from any device with a web browser.

|web_interface|

API
^^^

Time-series temperature, heating and cooling metrics may be consumed programatically using the *Braubuddy* API.

Outputs
^^^^^^^

*Braubuddy* outputs allow metric values to be recorded in a variety of formats or published directly to external services including Graphite, Librato, Dweet and Twitter.

Extensible
^^^^^^^^^^

The various *Braubuddy* components are designed to be extended. Consult ``CONTRIBUTE.RST`` if you'd like to request or contribute support for a particular component.

Getting Started
---------------

Hardware
^^^^^^^^

To monitor temperature using *Braubuddy* you will need a supported `thermometer <http://braubuddy.org/components.html#thermometer>`_.

To control temperature you will also need a supported `environmental controller <http://braubuddy.org/components.html#envcontroller>`_.

Install
^^^^^^^

*Braubuddy* is best enjoyed from within a Python `virtualenv <http://virtualenv.readthedocs.org/en/latest/>`_:

::

    virtualenv ~/braubuddy
    source ~/braubuddy/bin/activate

Production
~~~~~~~~~~

Install the latest production release from `PyPI <https://pypi.python.org/>`:

::

    pip install braubuddy

Development
~~~~~~~~~~~

Install the latest development release from `Github <https://github.com/amorphic/braubuddy>`_:

::

    git clone https://github.com/amorphic/braubuddy.git
    pip install -e ./braubuddy

Start
^^^^^

Start braubuddy with a single command:

::

    braubuddy

Configure
^^^^^^^^^

If not already present, a default configuration file is deployed to ``~/.config/braubuddy/``.

For system-wide configuration, copy this config file to ``/etc/xdg/braubuddy/``.

The example config file use default targets and automatically attempts to find a compatible thermometer and environmental controller. Follow `the docs <http://braubuddy.org/configure.html>`_ to customise your configuration. 


.. |travis| image:: https://travis-ci.org/amorphic/braubuddy.svg?branch=master
  :alt: Braubuddy CI
  :target: https://travis-ci.org/amorphic/braubuddy

.. |downloads| image:: https://pypip.in/download/braubuddy/badge.svg
  :alt: Downloads
  :target: https://pypi.python.org/pypi/braubuddy/

.. |versions| image:: https://pypip.in/py_versions/braubuddy/badge.svg
  :alt: Supported Python versions
  :target: https://pypi.python.org/pypi/braubuddy/

.. |logo| image:: images/logo/bb_logo_24x24.png
  :alt: Braubuddy web application
  :target: https://braubuddy.org

.. |web_interface| image:: /images/screenshots/1.png
  :alt: Braubuddy web application
  :target: https://braubuddy.org
