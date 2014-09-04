Install
=======

Hardware
^^^^^^^^

To monitor temperature using *Braubuddy* you will need a supported :ref:`thermometer <thermometer>`.

To control temperature you will also need a supported :ref:`environmental controller <envcontroller>`.

Virtualenv
----------

*Braubuddy* is best enjoyed from within a Python `virtualenv`_:
::

    virtualenv ~/braubuddy
    source ~/braubuddy/bin/activate

Production
----------

Install the latest production release from `PyPI`_ using `pip`_:

::

    pip install braubuddy

Development
-----------

Install the latest development release from `Github`_:

::

    git clone https://github.com/amorphic/braubuddy.git
    pip install -e ./braubuddy

Run
---

Run *Braubuddy*:

::

    braubuddy

*Braubuddy* will auto-detect your hardware and begin managing your environment. The *Braubuddy* web interface should be accessible by browsing to *http://<hostname>:8080*.

With *Braubuddy* up and running, the next step is to customise your :ref:`configuration`.

.. _`virtualenv`: http://virtualenv.readthedocs.org/en/latest/
.. _`PyPI`: https://pypi.python.org/ 
.. _`pip`: http://www.pip-installer.org/
.. _`Github`: https://github.com/amorphic/braubuddy/
