from enum import Enum


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    LOCKED = "locked"
    ACTIVATION_PENDING = "activation_pending"  # till user is not verified


class DeactivationReasons(Enum):
    NOT_DEACTIVATED = "not deactivated"
    SUSPICIOUS_REASON = "suspicious activity found"
    DELETE_REQUESTED = "account deletion request"


class HTTPStatusCodes(Enum):
    SUCCESS = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    FORBIDDEN = 403
    UNAUTHORIZED = 401
    MOVED_TEMPORARILY = 302
    INTERNAL_SERVER_ERROR = 500
    REQUEST_TIMEOUT = 408


class ORMConstant(Enum):
    DEFAULT_LIMIT = 100
    DEFAULT_OFFSET = 0
