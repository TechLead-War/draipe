class ExpectedDataNotFound(Exception):
    def __init__(self, message):
        self.message = message


class UserProcessingError(Exception):
    def __init__(self, message):
        self.message = message


class OperationalError(Exception):
    def __init__(self, message):
        self.message = message


class ProcessOrderError(Exception):
    def __init__(self, message):
        self.message = message


class InternalException(Exception):
    def __init__(self, exception, message=None, to_raise=True):
        self.exception = exception
        self.message = message
        self.to_raise = to_raise


class DBException(Exception):
    def __init__(self, exception, message=None, to_raise=True):
        self.exception = exception
        self.message = message
        self.to_raise = to_raise
