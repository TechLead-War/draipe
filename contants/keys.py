import secrets


class Keys:
    # This is the key that is used to remove extra data send in response.
    keys_to_remove = [
        'id',
        'password',
        '_partial',
        '_saved_in_db',
        '_custom_generated_pk',
        'reference_id'
    ]

    # This key is for validating user payload while creating user
    VALUE_MAPPING_FOR_USER = {
        "date_of_birth": {
            "db_value": "dob",
            "is_mandatory": True,
        },
        "personal_email_id": {"db_value": "email", "is_mandatory": False},
        "official_email_id": {"db_value": "work_email", "is_mandatory": False},
        "phone_number": {"db_value": "number", "is_mandatory": True},
        "reference_id": {
            "db_value": "reference_id",
            "is_mandatory": False,
        },
        "first_name": {"db_value": "first_name", "is_mandatory": True},
        "middle_name": {"db_value": "middle_name", "is_mandatory": False},
        "last_name": {"db_value": "last_name", "is_mandatory": False},
        "gender": {"db_value": "gender", "is_mandatory": True},
        "corporate_identifier": {
            "db_value": "corporate_identifier",
            "is_mandatory": False,
        },
        "address": {
            "db_value": "address",
            "is_mandatory": False,
        },
        "pin_code": {
            "db_value": "pin_code",
            "is_mandatory": False,
        },
        "address_type": {
            "db_value": "address_type",
            "is_mandatory": False,
        },
        "landmark": {
            "db_value": "landmark",
            "is_mandatory": False,
        },
    }


class Secret:
    # add this key in vault, and to be created once.
    JWT_secret_key = str(secrets.SystemRandom().getrandbits(256))
