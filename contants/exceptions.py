class UserProcessingError(Exception):
    def __init__(self, message):
        self.message = message


class OperationalError(Exception):
    def __init__(self, message):
        self.message = message
