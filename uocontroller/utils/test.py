"""Testing utilities for UOController."""

from uocontroller.cli.main import UOControllerTestApp
from cement.utils.test import *

class UOControllerTestCase(CementTestCase):
    app_class = UOControllerTestApp

    def setUp(self):
        """Override setup actions (for every test)."""
        super(UOControllerTestCase, self).setUp()

    def tearDown(self):
        """Override teardown actions (for every test)."""
        super(UOControllerTestCase, self).tearDown()

