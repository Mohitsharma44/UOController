"""UOController IR controller."""

from cement.ext.ext_argparse import ArgparseController, expose

class UOControllerIrController(ArgparseController):
    class Meta:
        label = 'IR'
        description = 'Controller for IR cameras'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            (['-l', '--loc'],
             dict(help='location of the cameras. e.g 1mtcNorth', dest='loc', action='store',
                  metavar='String') ),
            (['-c', '--capture'],
             dict(help="capture command", dest='capture', action='store_true')),
            (['-i', '--every'],
             dict(help="perform action every X seconds", dest='every', action='store',
                  metavar='String'))
            ]

    @expose(hide=True)
    def default(self):
        print("Inside UOControllerIrController.default().")
        if self.app.pargs.capture and self.app.pargs.every:
            print("Starting Capture: ", self.app.pargs.every)

        # If using an output handler such as 'mustache', you could also
        # render a data dictionary using a template.  For example:
        #
        #   data = dict(foo='bar')
        #   self.app.render(data, 'default.mustache')
        #
        #
        # The 'default.mustache' file would be loaded from
        # ``uocontroller.cli.templates``, or ``/var/lib/uocontroller/templates/``.
        #
