from asyncio.log import logger
from datetime import datetime

from argon2 import PasswordHasher as Argon2PasswordHasher
from argon2 import exceptions as argon2_exceptions
from sanic import Blueprint

from contants import DeactivationReasons, Keys, UserStatus
from contants.exceptions import (DBException, OperationalError,
                                 UserProcessingError, ValidationError)
from contants.messages import ErrorMessages
from managers.generals import fetch_record, value_mapper
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
        except argon2_exceptions.VerifyMismatchError:
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
        return await cls.filter_get_data(user_set[0].__dict__)

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
                    value["db_value"]: "not_found"
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
    async def delete_user(cls, user_id: str):
        """
            Deleting a user means deactivating the user status.
        """

        deletion_date = datetime.now()
        try:
            user_details = await fetch_record({
                "id": user_id
            })
            await ORMWrapper.update_with_filters(
                user_details[0],
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
    async def change_password(cls, user_req: dict):
        """

        """

        hasher = PasswordHasher()
        new_password = user_req.get("new_password")
        confirm_password = user_req.get("confirm_password")
        user_req = await value_mapper(user_req, Keys.PASSWORD_CHANGE_MAPPING.value)

        user_db = await fetch_record(filters={
            "username": user_req.get("username")
        })
        if not user_db:
            raise DBException(message="Unable to fetch user details from DB!!")

        user_db_dict = user_db[0].__dict__
        user_pass = user_db_dict.get("password")

        current_password = user_req.get("password")

        # Verify current password,
        # user_pass: current password from database
        # user_data->current_pass: password captured from user request

        if hasher.verify_password(current_password, user_pass):
            if confirm_password == new_password:
                # hash the pass
                hashed_password = hasher.hash_password(new_password)
                # update the password in db
                await ORMWrapper.update_with_filters(
                    user_db[0],
                    Users,
                    {
                        "updated_on": datetime.now(),
                        "password": hashed_password
                    },
                    update_fields=cls.update_fields,
                )
                return {
                    "data": {
                        "is_success": True
                    },
                    "status_code": 200
                }
            else:
                raise UserProcessingError("Password not matched, "
                                          "new password and confirm "
                                          "password should be same!!")
        else:
            raise UserProcessingError("Password not matched, current "
                                      "password and your account password !!")

    @classmethod
    async def update_user(cls, user_details: dict, update_data: dict):

        """
            This function update user in users db

            Args:
                user_details: username of the updating user.
                update_data: Details of user that needs to be updated

            Returns:
                True on successful update, False otherwise
        """

        #  what details can't be updated, and who can update.
        #  check from context if it's the correct user

        try:
            user_details = await fetch_record(user_details)
            update_data.update({
                "updated_on": datetime.now()
            })
            if user_details:
                await ORMWrapper.update_with_filters(
                    user_details[0],
                    Users,
                    update_data,
                    update_fields=cls.update_fields,
                )
                return {
                    "data": {
                        "is_success": True
                    },
                    "status_code": 200
                }
            else:
                logger.error(f"User with details '{user_details}' not found!")
                return {
                    "data": {
                        "is_success": True,
                        "description": f"User with details '{user_details}' "
                                       f"not found!"
                    },
                    "status_code": 400
                }

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

# Forgot Password: An API endpoint that handles the process of resetting a
# user's forgotten password, typically by sending a password reset link via
# email.

# User Preferences: APIs to manage user preferences, such as language
# preferences, notification settings, theme selection, etc.

# Order History: An API endpoint to fetch the order history of a user,
# including details like order ID, products ordered, payment status,
# delivery status, etc.

# Wishlist: APIs to manage a user's wishlist, allowing them to add products,
# remove products, or view their saved wishlist. ** DB change may required.

# Address Book: APIs to manage a user's address book, allowing them to add,
# update, or delete their shipping addresses for easy checkout.

# Account Deactivation: An API endpoint to handle account deactivation or
# closure, providing users with an option to permanently delete their account.

# Email Subscription: APIs to manage a user's email subscriptions,
# allowing them to subscribe or unsubscribe from newsletters,
# promotional emails, etc.

# Social Authentication: APIs to support social authentication,
# allowing users to log in or register using their social media
# accounts like Facebook, Google, or Twitter.
