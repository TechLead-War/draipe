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


class Roles(Enum):
    ROLE_ADMIN = "ROLE_ADMIN"
    ROLE_USER = "ROLE_USER"
    ROLE_SUB_ADMIN = "ROLE_SUB_ADMIN"


class OrderStatusTypes(Enum):
    ORDER_PLACED = "order placed."
    SYSTEM_APPROVAL_PENDING = "system approval pending."
    SYSTEM_APPROVED = "system approved, will be shipped soon."
    USER_CONSENT_PENDING = "user consent pending"
    USER_APPROVED = "user approved"
    USER_DECLINED = "user declined"
    ORDER_CANCELLED = "order cancelled"
    ORDER_PROCESSED = "order processed"
