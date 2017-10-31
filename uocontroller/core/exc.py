"""UOController exception classes."""

class UOControllerError(Exception):
    """Generic errors."""
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg

class UOControllerConfigError(UOControllerError):
    """Config related errors."""
    pass

class UOControllerRuntimeError(UOControllerError):
    """Generic runtime errors."""
    pass

class UOControllerArgumentError(UOControllerError):
    """Argument related errors."""
    pass
