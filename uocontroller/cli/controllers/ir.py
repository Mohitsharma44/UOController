"""UOController IR controller."""

import os
import json
import subprocess
from cement.ext.ext_argparse import ArgparseController, expose
from uocontroller.cli.controllers.rpc_client import UOControllerRpcClient

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
                  metavar='String')),
            (['--live', '--live'],
             dict(help="Open Live Feed to the camera", dest='live', action='store_true'))
            ]

    def _generate_data(self):
        return {
            "location": self.app.pargs.loc,
            "capture": self.app.pargs.capture,
            "interval": self.app.pargs.every,
            }
        
    @expose(hide=True)
    def default(self):
        ir_rpc_client = UOControllerRpcClient(queue_name="uoir_queue")
        print("Inside UOControllerIrController.default().")
        command = self._generate_data()
        print(ir_rpc_client.call(json.dumps(command)))
        if self.app.pargs.live:
            print("Opening Live Stream ... ")
            proc = subprocess.Popen(["vlc", "rtsp://{}".format(os.environ['south_ircam_ip'])],
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE)
            out, err = proc.communicate()
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
