"""UOController IR controller."""

import os
import json
import subprocess
from cement.ext.ext_argparse import ArgparseController, expose
from uocontroller.cli.controllers.rpc_client import UOControllerRpcClient

known_ir_queues = {
        "1mtcNorth": "1mtcNorth_ir_queue",
        "1mtcSouth": "1mtcSouth_ir_queue",
        "370Roof"  : "370Roof_ir_queue",
        "test"     : "test_ir_queue"
    }

class QueueNameException(Exception):
    pass

class UOControllerIrController(ArgparseController):

    class Meta:
        
        label = 'IR'
        description = 'Controller for IR cameras'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            (['-l', '--loc'],
             dict(help='location of the cameras. e.g: \n\t 1mtcNorth \n\t 1mtcSouth \n\t 370Roof(WIP) \n\t test(WIP)',
                  dest='loc', action='store', metavar='String')),
            (['-c', '--capture'],
             dict(help="capture X frames (use -1 to capture forever)", dest='capture', action='store',
                  default=0, const=0, nargs='?', metavar='Int')),
            (['--every', '--every'],
             dict(help="perform capture every X seconds. default is 10s", dest='every', action='store',
                  metavar='Int', default=0, const=0, nargs='?')),
            (['--live', '--live'],
             dict(help="Open Live Feed to the camera (Not Implemented)", dest='live', action='store_true')),
            (['-f', '--focus'],
             dict(help="Focus the vis camera camera. options=<absolute value>", dest='focus', action='store',
                  metavar='float', default=-1, const=-1, nargs='?')),
            (['-s', '--stop'],
             dict(help="Abort and Stop acquiring images", dest='stop', action='store_true', default=0)),
            (['-stat', '--status'],
             dict(help="Current Status of the camera and its driver", dest='stat', action='store_true', default=False)),
            (['--kill', '--kill'],
             dict(help="""This will kill the code driving the camera on the remote end. Make sure you do want to
             do this. There is a chance that the driving code will be restarted automatically but cannot be
             guaranteed.""", dest='kill', action='store', default='', metavar='String')),
            (['-z', '--zoom'],
             dict(help="Digital Zoom factor between 1 and 8. default is 1", dest='zoom', action='store',
                  metavar='float', default=-1, const=-1, nargs='?')),
            ]

    def _generate_data(self):
        return {
            "location": self.app.pargs.loc,
            "capture": True if int(self.app.pargs.capture) != 0 else False,
            "count": int(self.app.pargs.capture),
            "interval": int(self.app.pargs.every),
            "zoom": int(self.app.pargs.zoom),
            "focus": int(self.app.pargs.focus),
            "stop": bool(self.app.pargs.stop),
            "status": bool(self.app.pargs.stat),
            }

    @expose(hide=True)
    def default(self):
        if not self.app.pargs.loc in known_ir_queues.keys():
            raise QueueNameException("Check the location name format!!")

        ir_rpc_client = UOControllerRpcClient(vhost="/ir",
                                              queue_name=known_ir_queues[self.app.pargs.loc])
        print("Inside UOControllerIrController.default().")
        # Generate Json structured command
        try:
            if not self.app.pargs.loc:
                print("You need to pass the location")
                sys.exit(1)
            command = self._generate_data()
            print(ir_rpc_client.call(json.dumps(command)))
        except Exception as ex:
            print("Error generating json structured command: ", str(ex))
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
