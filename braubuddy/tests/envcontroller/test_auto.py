"""
Braubuddy Auto envcontroller unit tests.
"""

from mock import patch, call, MagicMock
from braubuddy.tests import BraubuddyTestCase
from braubuddy.envcontroller import auto 
from braubuddy.envcontroller import dummy 
from braubuddy.envcontroller import tosr0x_usb 

class TestAuto(BraubuddyTestCase):

    @patch('braubuddy.envcontroller.tosr0x_usb.tosr0x')
    def test_dummy_returned_if_no_devices(self, mk_tosr0x):
        """Dummy envcontroller is created if no real envcontrollers discovered."""

        mk_tosr0x.handler.return_value = []
        envcontroller = auto.AutoEnvController()
        self.assertIsInstance(envcontroller, dummy.DummyEnvController)
