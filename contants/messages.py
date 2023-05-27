from enum import Enum


class ErrorMessages(Enum):
    EMAIL_NOT_FOUND = "Email address is missing"
    API_KEY_ERROR = "Exception occurred on {} API"
    DUPLICATE_USER = "{} already exists, please try to login"
    DUPLICATE_ITEM = "Duplicate value of {} already exists"
    USER_ALREADY_PRESENT = "User with these details already present."
    MOBILE_ALREADY_PRESENT = "Mobile number linked to a different account"
    ACTION_TYPE_ERROR = "Action can be of type add, update, delete"
    USER_CREATE_ERROR = "Unable to create user"
    USER_ADD_ADDRESS_ERROR = (
        "Unable to add address due to incomplete address details"
    )
    UPDATE_UPDATE_ERROR = "Unable to update user"
    USER_DELETE_ERROR = "Unable to delete user"
    USER_ALREADY_INACTIVE = "Corporate account already expired"
    USER_ALREADY_ACTIVE = "User account already active"
    INVALID_DATE = "Incorrect date format, should be YYYY-MM-DD"
    INVALID_GENDER = "Invalid gender"
    REFERENCE_ID_ERROR = "reference_id is incorrect or missing"
    MOBILE_NUMBER_ALREADY_EXISTS_ERROR = (
        "Mobile number linked to a different account."
    )
    ENTITY_NOT_FOUND = "{} not found"
    ORDER_NOT_FOUND = "Order with order id '{}' does not exists"
    USER_NOT_FOUND = "User {} not found"
    START_TIME_ERROR = (
        "Start time must be greater than or equal to current time"
    )
    START_END_TIME_ERROR = "Start time must be less than end time"
    END_TIME_ERROR = "End time must be greater than or equal to current time"
    SUSPENSION_REASON_NOT_FOUND = "Please provide a reason for suspension"
    UNABLE_TO_PROCESS = "Unable to process the request"
    UNABLE_TO_SUSPEND = "Unable to process suspend request"
    UNABLE_TO_RESUME = "Unable to active the user"
    INVALID_ORDER_ID_ERROR = "This Order id does not belong to us"
    INVALID_TOKEN_ERROR = "Invalid token or Token Expired"
    ORDER_CANCELLED_ERROR = "Order already cancelled or does not exist"
    ORDER_ID_EXIST_ERROR = "Order id already exists"
    ORDER_ALREADY_CANCELLED = "Order is already cancelled"
    ORDER_ALREADY_MOVED = (
        "Order already moved to vendor stock allocation stage"
    )
    USERNAME_NOT_FOUND = "Username not found"
    USERNAME_MIGRATION_FAILED = "username migration failed"
    UNABLE_TO_PROCESS_ORDER = "Unable to process order further"
    INVALID_USER_ERROR = "This user does not belong to us"
    UNABLE_TO_FETCH_USER = "Unable to fetch user"
    FILE_NOT_FOUND = "Requested file is not available"
    INVALID_NUMBER = "Invalid phone number"
    PRESIGNED_URL_ERROR = "Not able to generate Presigned URL."

