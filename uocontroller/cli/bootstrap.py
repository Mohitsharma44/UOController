"""UOController bootstrapping."""

# All built-in application controllers should be imported, and registered
# in this file in the same way as UOControllerBaseController.

from uocontroller.cli.controllers.base import UOControllerBaseController
from uocontroller.cli.controllers.ir import UOControllerIrController

def load(app):
    app.handler.register(UOControllerBaseController)
    app.handler.register(UOControllerIrController)
