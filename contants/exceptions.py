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


class ValidationError(Exception):
    def __init__(self, message):
        self.message = message


class ResetPasswordError(Exception):
    """Base exception for reset password errors."""
    def __init__(self, message):
        self.message = message


class UserNotFoundError(ResetPasswordError):
    """Exception raised when the user is not found."""
    def __init__(self, message):
        self.message = message


class InvalidTokenError(ResetPasswordError):
    """Exception raised when the reset password token is invalid."""
    def __init__(self, message):
        self.message = message


class ExpiredTokenError(ResetPasswordError):
    """Exception raised when the reset password token has expired."""
    def __init__(self, message):
        self.message = message
