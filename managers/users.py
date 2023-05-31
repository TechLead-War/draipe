from asyncio.log import logger

from argon2 import PasswordHasher as Argon2PasswordHasher
from datetime import datetime

from sanic import Blueprint

from contants import Keys, UserStatus, DeactivationReasons
from contants.exceptions import UserProcessingError, DBException, \
    OperationalError, ValidationError
from contants.messages import ErrorMessages
from managers.generals import fetch_record
from managers.orm_wrappers import ORMWrapper
from models.users import Users
from utils.helpers import (is_email_or_phone_taken, is_valid_dob,
                           is_valid_gender, is_valid_number, serialize_date)
from utils.parsers import rectify_payload, to_string

user = Blueprint("users", url_prefix="/user")


class PasswordHasher:
    def __init__(self):
        self.ph = Argon2PasswordHasher()

    def hash_password(self, password):
        """
        Hashes the provided password using Argon2.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        return self.ph.hash(password)

    def verify_password(self, password, hashed_password):
        """
        Verifies if the provided password matches the hashed password.

        Args:
            password (str): The password to verify.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        try:
            self.ph.verify(hashed_password, password)
            return True
        except:
            return False


class UserManager:
    update_fields = [
        "first_name",
        "last_name",
        "created_on",
        "updated_on",
        "email",
        "dob",
        "number",
        "number_code",
        "gender",
        "metadata",
        "status",
        "username",
        "premium_user",
        "premium_buy_on",
        "reference_id",
        "password",
        "deactivation_reason",
        "profile_picture",
        "address_id",
        "is_email_verified",
        "is_number_verified",
        "is_loyal_customer",
    ]

    @classmethod
    async def filter_get_data(cls, raw_data: dict):
        keys_to_remove = Keys.keys_on_get_request.value
        return {key: value for key, value in raw_data.items() if key not in
                keys_to_remove}

    @classmethod
    async def get_user_details(cls, user_id: str):

        #  what all details can be shared.
        user_details = {}
        if user_id.startswith("draipe_"):
            user_details.update({
                "username": user_id
            })
        else:
            user_details.update({
                "id": user_id
            })
        user_set = await fetch_record(user_details)
        return await cls.filter_get_data(user_set)

    @classmethod
    async def verify_user_data(cls, user_payload: dict,
                               user_value_mapping: dict):
        """
            This function maps user data with db values and
            create a new user dictionary, and checks if all
            required values are given in payload to create
            user.

            Args:
                user_payload: original user data

                user_value_mapping: A dictionary that contains value
                mapping of original user data and our internal DB values
                it also tells which data is mandatory.

            Returns:
                Dict containing processed user data
        """

        # check if all required fields are present.
        resultant_user_data = dict()
        for key, value in user_value_mapping.items():
            if value["is_mandatory"]:
                if not user_payload.get(key, {}):
                    raise UserProcessingError(
                        f"Missing {key} in beneficiary data"
                    )
            if user_payload.get(key):
                resultant_user_data.update({
                    value["db_value"]: user_payload[key]
                })
            else:
                resultant_user_data.update({
                    value["db_value"]: "user_payload[key]"
                })

        # populate system generated values
        resultant_user_data["created_on"] = str(datetime.now().isoformat())
        resultant_user_data["dob"] = serialize_date(resultant_user_data["dob"])
        resultant_user_data["metadata"] = ""
        resultant_user_data["status"] = UserStatus.ACTIVE.value
        resultant_user_data["referral_id"] = "12"

        # generate the hash and change the plain text to protected value.
        hasher = PasswordHasher()
        resultant_user_data["password"] = hasher.hash_password(
            resultant_user_data["password"]
        )

        return resultant_user_data

    @classmethod
    async def validate_user_data(cls, user_data: dict):
        """
            This function validate data, like
            duplicate emails,
            already present phone, and other info
            incorrect format of any details

        """
        if not is_valid_dob(user_data["dob"]):
            raise UserProcessingError(ErrorMessages.INVALID_DATE.value)
        if not is_valid_gender(user_data["gender"]):
            raise UserProcessingError(ErrorMessages.INVALID_GENDER.value)
        if not is_valid_number(user_data["number"]):
            raise UserProcessingError(
                ErrorMessages.INVALID_NUMBER.value
            )
        if await is_email_or_phone_taken(user_data["email"],
                                         user_data["number"]):
            raise UserProcessingError(ErrorMessages.USER_ALREADY_PRESENT.value)

    @classmethod
    async def create_user(cls, payload: dict):
        """
            Verify if all data required is given, and populate some system
            generate values in payload for further processing.
        """

        user_mapping = Keys.VALUE_MAPPING_FOR_USER.value
        user_data = await cls.verify_user_data(
            payload, user_mapping
        )

        # validate user
        await cls.validate_user_data(user_data)

        # hash password

        # create user in our database
        new_user = await ORMWrapper.create(Users, user_data)
        new_user = new_user.__dict__  # convert object to dict
        new_user = await rectify_payload(new_user)
        new_user = to_string(new_user)
        return new_user

    @classmethod
    async def delete_user(cls, number: str):
        """
            Deleting a user means deactivating the user status.
        """

        deletion_date = datetime.now()
        try:
            user_details = await fetch_record({
                "number": number
            })

            await ORMWrapper.update_with_filters(
                user_details,
                Users,
                {
                    "updated_on": deletion_date,
                    "status": UserStatus.INACTIVE.value,
                    "deactivation_reason":
                        DeactivationReasons.DELETE_REQUESTED.value
                },
                update_fields=cls.update_fields,
            )
        except DBException as ex:
            pass
        except UserProcessingError as ex:
            pass

    @classmethod
    async def change_password(cls, user_data: dict):
        """

        """

        username = user_data.get("username")
        user_set = await fetch_record(username)
        user_pass = user_set.get("password")
        new_password = user_set.get("new_password")
        confirm_password = user_set.get("confirm_password")

        hasher = PasswordHasher()

        # Check if user exists
        if username and user_set:
            current_pass_from_db = await fetch_record({
                "username": username
            })
            # Verify current password
            if hasher.verify_password(user_pass, current_pass_from_db):
                if confirm_password == new_password:
                    # hash the pass
                    hashed_password = hasher.hash_password(new_password)

                    # update the password in db
                    await ORMWrapper.update_with_filters(
                        current_pass_from_db,
                        Users,
                        {
                            "updated_on": datetime.now(),
                            "password": hashed_password
                        },
                        update_fields=cls.update_fields,
                    )
                else:
                    raise UserProcessingError("Password not matched, "
                                              "new password and confirm "
                                              "password")
            else:
                raise UserProcessingError("Password not matched, current "
                                          "password and new password !!")
        else:
            raise UserProcessingError("User not found")

    @classmethod
    async def update_user(cls, username: str, update_data: dict):

        """
            This function update user in users db

            Args:
                update_data: Details of user that needs to be updated
                username: username of the updating user.

            Returns:
                True on successful update, False otherwise
        """

        #  what details can't be updated, and who can update.
        #  check from context if it's the correct user

        try:
            user_detail = await ORMWrapper.get_by_filters(
                Users, {"username": username}
            )
            user_detail = user_detail[0]

            await ORMWrapper.update_with_filters(
                user_detail,
                Users,
                update_data,
                update_fields=cls.update_fields,
            )
            return True

        except (ValueError, OperationalError, ValidationError) as ex:
            logger.exception(
                f"Exception occurred while updating user details!"
            )
            return False

    @classmethod
    async def remove_expired_users(cls):
        deletion_date = datetime.now() - timedelta(days=30)
        expired_users = await cls.filter(deleted_on__lte=deletion_date)
        await expired_users.delete()

