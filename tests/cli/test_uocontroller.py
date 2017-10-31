"""CLI tests for uocontroller."""

from uocontroller.utils import test

class CliTestCase(test.UOControllerTestCase):
    def test_uocontroller_cli(self):
        argv = ['--foo=bar']
        with self.make_app(argv=argv) as app:
            app.run()
            self.eq(app.pargs.foo, 'bar')
