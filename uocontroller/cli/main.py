"""UOController main application entry point."""

from cement.core.foundation import CementApp
from cement.utils.misc import init_defaults
from cement.core.exc import FrameworkError, CaughtSignal
from uocontroller.core import exc

# Application default.  Should update config/uocontroller.conf to reflect any
# changes, or additions here.
defaults = init_defaults('uocontroller')

# All internal/external plugin configurations are loaded from here
#defaults['uocontroller']['plugin_config_dir'] = '/etc/uocontroller/plugins.d'
defaults['uocontroller']['plugin_config_dir'] = './plugins'

# External plugins (generally, do not ship with application code)
#defaults['uocontroller']['plugin_dir'] = '/var/lib/uocontroller/plugins'
defaults['uocontroller']['plugin_dir'] = './plugins'

# External templates (generally, do not ship with application code)
#defaults['uocontroller']['template_dir'] = '/var/lib/uocontroller/templates'
defaults['uocontroller']['template_dir'] = './templates'


class UOControllerApp(CementApp):
    class Meta:
        label = 'uocontroller'
        config_defaults = defaults
        # override configuration with commandline options
        arguments_override_config = True
        # All built-in application bootstrapping (always run)
        bootstrap = 'uocontroller.cli.bootstrap'

        # Internal plugins (ship with application code)
        plugin_bootstrap = 'uocontroller.cli.plugins'

        # Internal templates (ship with application code)
        template_module = 'uocontroller.cli.templates'

        # call sys.exit() when app.close() is called
        exit_on_close = True

        extensions = ['mustache', 'json', 'yaml']
        handler_override_options = dict(
            output = (['-o'], dict(help='output format')),
        )


class UOControllerTestApp(UOControllerApp):
    """A test app that is better suited for testing."""
    class Meta:
        # default argv to empty (don't use sys.argv)
        argv = []

        # don't look for config files (could break tests)
        config_files = []

        # don't call sys.exit() when app.close() is called in tests
        exit_on_close = False


# Define the applicaiton object outside of main, as some libraries might wish
# to import it as a global (rather than passing it into another class/func)
app = UOControllerApp()

def main():
    with app:
        try:
            app.run()
            #data = {"foo": app.pargs.loc}
            #app.render(data, 'default.m')
        
        except exc.UOControllerError as e:
            # Catch our application errors and exit 1 (error)
            print('UOControllerError > %s' % e)
            app.exit_code = 1
            
        except FrameworkError as e:
            # Catch framework errors and exit 1 (error)
            print('FrameworkError > %s' % e)
            app.exit_code = 1
            
        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('CaughtSignal > %s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
