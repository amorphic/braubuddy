|logo| Braubuddy
================

|travis|

*Braubuddy* is a temperature management framework written in Python.

Conceived as a means of monitoring and controlling the fermentation temperature of beer, *Braubuddy* can be used in any situation requiring precise temperature control:

- Keep tropical fish swimming happily in water that's 26°C 
- Brew a perfect lager by fermenting at a constant 9°C
- Maximise employee productivity with an optimum office ambient air temp of 21.5°C

Features
--------

Web Interface
^^^^^^^^^^^^^

*Braubuddy*'s web interface facilitates temperature monitoring from any device with a web browser:

.. image:: ../images/screenshots/1.png

API
^^^

Time-series temperature, heating and cooling metrics may be consumed programatically using the *Braubuddy* :ref:`API`.

Outputs
^^^^^^^

*Braubuddy* :ref:`outputs <output>` allow metric values to be recorded in a variety of formats or published directly to external services.

Extensible
^^^^^^^^^^

The various *Braubuddy* :ref:`components` are designed to be extended. Consult the :ref:`guidelines <contribute>` if you'd like to request or contribute support for a particular component.Getting Started
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

::
    braubuddy

Configure
~~~~~~~~~

If not already present, a default configuration file is deployed to ``~/.config/braubuddy/``.

For system-wide configuration, copy this config to ``/etc/xdg/braubuddy/``.

The example config file use default targets and automatically attempts to find a compatible thermometer and environmental controller. Follow `the docs <http://braubuddy.org/configure>`_ to customise your configuration. 


.. |travis| image:: https://travis-ci.org/amorphic/braubuddy.svg?branch=master
  :alt: Braubuddy CI
  :target: https://travis-ci.org/amorphic/braubuddy

.. |logo| image:: images/logo/bb_logo_24x24.png
  :alt: Braubuddy web application
  :target: https://github.com/amorphic/braubuddy

.. |screenshot_1| image:: /images/screenshots/1.png
  :alt: Braubuddy web application
  :target: https://github.com/amorphic/braubuddy

