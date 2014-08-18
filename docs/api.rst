.. _API:

API
==========

Metrics collected during each Braubuddy cycle are stored and made available via ``GET`` requests to an API endpoint:

::

    http://<hostname>:<port>/api/

Metrics values are presented in time series in the format:

``[_target temp_, _actual temp_, _heat level_, _cool_level, _epoch timestamp_]``

e.g.

::

    [[28.0, 25.5, 0, 0, 1402990571], [28.0, 27.25, 0, 100, 1402990631], [28.0, 28.5, 0, 100, 1402990692],
    [28.0, 29.375, 0, 100, 1402990754], [28.0, 30.0, 0, 100, 1402990815], [28.0, 30.25, 0, 100, 1402990876],
    [28.0, 30.375, 0, 100, 1402990937], [28.0, 30.5, 0, 100, 1402990999], [28.0, 30.375, 0, 100, 1402991060],
    [28.0, 30.375, 0, 100, 1402991121], [28.0, 30.5, 0, 100, 1402991182], [28.0, 30.375, 0, 100, 1402991243],
    [28.0, 30.375, 0, 100, 1402991305], [28.0, 30.75, 0, 100, 1402991366], [28.0, 30.875, 0, 100, 1402991427],
    [28.0, 31.125, 0, 100, 1402991488]]

Parameters
----------

A number of `query string`_ parameters are available to limit the datapoints returned:

==========  =============== =======================================================
Parameter   Type            Description
==========  =============== =======================================================
``since``   int (timestamp) Limit results to datapoints with timetamps > ``since``
``before``  int (timestamp) Limit results to datapoints with timetamps < ``before``
``limit``   int             Limit number of results returned to ``limit``
==========  =============== =======================================================

Thus this URL:

::

    http://mybraubuddyhost:8080/api?since=1402990630&before=1402991430&limit=3
    
Would yield the following subset of the data returned in the example above:

::

    [[28.0, 27.25, 0, 100, 1402990631], [28.0, 28.5, 0, 100, 1402990692]]
    [28.0, 29.375, 0, 100, 1402990754]]
    
.. _`query string`: http://en.wikipedia.org/wiki/Query_string/
