from datetime import datetime

from sanic import Blueprint
import password

from contants import Keys, UserStatus
from contants.exceptions import UserProcessingError
from contants.messages import ErrorMessages
from models.users import Users
from models.orm_wrappers import ORMWrapper
from utils.helpers import is_valid_dob, is_valid_gender, is_valid_number, \
    is_email_or_phone_taken
from utils.parsers import rectify_payload

user = Blueprint("users", url_prefix="/user")


class UserManager:
    @classmethod
    async def get_user_details(cls, user_id: str):
        pass
        #  what all details can be shared.

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
                if not user_payload[key]:
                    raise UserProcessingError(
                        f"Missing {key} in beneficiary data"
                    )
        # populate system generated values
        user_payload["created_on"] = str(datetime.now())
        user_payload["dob"] = str(user_payload["dob"])
        user_payload["metadata"] = ""
        user_payload["status"] = UserStatus.ACTIVE.value

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
        # user already present - DUPLICATE_USER: errormsg
        await is_email_or_phone_taken(user_data["email"], user_data["phone"])
        if not is_valid_number(user_data["number"]):
            raise UserProcessingError(
                ErrorMessages.INVALID_NUMBER.value
            )

    @classmethod
    async def create_user(cls, payload: dict):
        #  verify if we require a check for non-null values.
        beneficiary_mapping = Keys.VALUE_MAPPING_FOR_USER.value
        user_data = await cls.verify_user_data(
            payload, beneficiary_mapping
        )

        # validate user
        await cls.validate_user_data(user_data)

        # create user in our database
        new_user = await ORMWrapper.create(Users, payload)
        new_user = new_user.__dict__  # convert object to dict
        return await rectify_payload(new_user)

    @classmethod
    async def update_user(cls, user_id: str, update_data: dict):
        #  what details can't be updated, and how can update.
        # check from context if it's the correct user

        invalid_fields = ["id", "created_on", "updated_on"]
        invalid_values = [None, ""]

        for field, value in update_data.items():
            if field in invalid_fields:
                continue
            if field not in self._meta.fields_map:
                raise ValueError(f"Invalid field: {field}")
            if value in invalid_values:
                raise ValueError(f"Invalid value for field {field}")

            setattr(self, field, value)

        await self.save()

    @classmethod
    async def delete_user(cls, user_id: str):
        """
            Deleted user will be kept for 30 days, and then data will be
            removed after 30-days from a cron-job.
        """

        deletion_date = datetime.now() + timedelta(days=30)
        self.deleted_on = deletion_date
        await self.save()

    @classmethod
    async def remove_expired_users(cls):
        deletion_date = datetime.now() - timedelta(days=30)
        expired_users = await cls.filter(deleted_on__lte=deletion_date)
        await expired_users.delete()

