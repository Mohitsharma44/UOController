"""Tests for Example Plugin."""

from uocontroller.utils import test

class ExamplePluginTestCase(test.UOControllerTestCase):
    def test_load_example_plugin(self):
        self.app.setup()
        self.app.plugin.load_plugin('example')
