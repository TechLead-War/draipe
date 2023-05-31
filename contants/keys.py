import secrets
from enum import Enum


class Keys(Enum):
    # This is the key that is used to remove extra data send in response.
    keys_to_remove = [
        'id',
        'password',
        '_partial',
        '_saved_in_db',
        '_custom_generated_pk',
        'reference_id'
    ]

    keys_on_get_request = [
        "id",
        "password",
        "created_on",
        "updated_on",
        "number_code",
        "metadata",
        "status",
        "username",
        "premium_user",
        "premium_buy_on",
        "reference_id",
        "password",
        "deactivation_reason",
        "address_id",
    ]

    # This key is for validating user payload while creating user
    VALUE_MAPPING_FOR_USER = {
        "first_name": {
            "db_value": "first_name",
            "is_mandatory": True,
        },
        "last_name": {
            "db_value": "last_name",
            "is_mandatory": True
        },
        "email_id": {
            "db_value": "email",
            "is_mandatory": True
        },
        "date_of_birth": {
            "db_value": "dob",
            "is_mandatory": True
        },
        "phone_number": {
            "db_value": "number",
            "is_mandatory": True
        },
        "phone_number_code": {
            "db_value": "number_code",
            "is_mandatory": True
        },
        "gender": {"db_value": "gender", "is_mandatory": True},
        "user_status": {
            "db_value": "status",
            "is_mandatory": False,
        },
        "reference_id": {
            "db_value": "reference_id",
            "is_mandatory": False,
        },
        "user_password": {
            "db_value": "password",
            "is_mandatory": False,
        },
        "user_profile_photo_url": {
            "db_value": "profile_picture",
            "is_mandatory": False,
        },
        "user_address": {
            "db_value": "address_id",
            "is_mandatory": False,
        },  # this will not be mapped to address id
    }


class Secret:
    # add this key in vault, and to be created once.
    JWT_secret_key = str(secrets.SystemRandom().getrandbits(256))


class RetryRequestConstant(Enum):
    """
    This class contains constant used in retrying
    API calls
    """

    RETRY_TIME = 5 * 10
    BACK_OFF_FACTOR = 2
    NO_OF_RETRY = 3
