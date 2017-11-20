"""UOController Vis controller."""

import os
import sys
import json
from cement.ext.ext_argparse import ArgparseController, expose
from uocontroller.cli.controllers.rpc_client import UOControllerRpcClient

class UOControllerVisController(ArgparseController):
    class Meta:
        label = 'VIS'
        description = 'Controller for Vis cameras'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            (['-l', '--loc'],
             dict(help='location of the cameras. e.g 1mtcNorth', dest='loc', action='store',
                  metavar='String') ),
            (['-c', '--capture'],
             dict(help="capture command", dest='capture', action='store_true')),
            (['--every', '--every'],
             dict(help="perform capture every X seconds. default is 10s", dest='every', action='store',
                  metavar='String')),
            (['--live', '--live'],
             dict(help="Open Live Feed to the camera", dest='live', action='store_true')),
            (['-f', '--focus'],
             dict(help="Focus the vis camera camera. options=<absolute value>", dest='focus', action='store'))
            ]

    def _generate_data(self):
        return {
            "location": self.app.pargs.loc,
            "capture": self.app.pargs.capture,
            "interval": self.app.pargs.every,
            "focus": self.app.pargs.focus,
            }
        
    @expose(hide=True)
    def default(self):
        vis_rpc_client = UOControllerRpcClient(queue_name="uovis_queue")
        print("Inside UOControllerVisController.default().")
        # Generate Json structured command
        try:
            if not self.app.pargs.loc:
                print("You need to pass the location")
                sys.exit(1)
            command = self._generate_data()
            print(vis_rpc_client.call(json.dumps(command)))
        except Exception as ex:
            print("Error generating json structured command: ", str(ex))
        if self.app.pargs.live:
            print("Feture not implemented ... ")
            
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
