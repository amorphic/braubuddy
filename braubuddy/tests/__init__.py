# Import unittest2 for Py 2.6.
try:
    import unittest2 as unittest
except ImportError:
    import unittest

class BraubuddyTestCase(unittest.TestCase):
    pass
