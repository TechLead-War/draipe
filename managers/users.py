from datetime import datetime

from sanic import Blueprint
import password

from contants import Keys, UserStatus
from contants.exceptions import ProcessBeneficiaryError
from models.users import Users
from models.orm_wrappers import ORMWrapper
from utils.parsers import rectify_payload

user = Blueprint("users", url_prefix="/user")


class UserManager:
    @classmethod
    async def get_user_details(cls, user_id: str):
        pass
        #  what all details can be shared.

    @classmethod
    async def verify_build_user_data(cls, user_payload: dict,
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

        # populate system generated values
        user_payload["created_on"] = str(datetime.now())
        user_payload["dob"] = str(user_payload["dob"])
        user_payload["metadata"] = ""
        user_payload["status"] = UserStatus.ACTIVE.value

        # check if all required fields are present.
        resultant_user_data = dict()
        for key, value in user_value_mapping.items():
            if value["is_mandatory"]:
                if not user_payload[key]:
                    raise ProcessBeneficiaryError(
                        f"Missing {key} in beneficiary data"
                    )

            if value["db_value"] == "metadata":
                if "metadata" in resultant_user_data:
                    resultant_user_data["metadata"].update(
                        {key: resultant_user_data.get(key)}
                    )
                else:
                    resultant_user_data["metadata"] = {
                        key: resultant_user_data.get(key)
                    }

            else:
                resultant_user_data[value["db_value"]] = \
                    resultant_user_data.get(key, "")

        if not beneficiary.get("name"):
            beneficiary["name"] = ""
            if beneficiary_data.get("first_name"):
                beneficiary["name"] += beneficiary_data.get("first_name")

            if beneficiary_data.get("middle_name"):
                beneficiary["name"] += " " + beneficiary_data.get(
                    "middle_name"
                )

            if beneficiary_data.get("last_name"):
                beneficiary["name"] += " " + beneficiary_data.get("last_name")

        key_name_list = list(beneficiary_value_mapping.keys())
        for key, value in beneficiary_data.items():
            if key not in key_name_list:
                if "metadata" in beneficiary:
                    beneficiary["metadata"].update(
                        {key: beneficiary_data.get(key)}
                    )
                else:
                    beneficiary["metadata"] = {key: beneficiary_data.get(key)}

        return resultant_user_data

    @classmethod
    async def validate_beneficiary_data(cls, user_data: dict):
        """
            This function validate data, like duplicate emails, etc.

        """
        pass

    @classmethod
    async def create_user(cls, payload: dict):
        #  verify if we require a check for non-null values.
        beneficiary_mapping = Keys.VALUE_MAPPING_FOR_USER.value
        user_data = await cls.verify_build_user_data(
            payload, beneficiary_mapping
        )

        # validate user
        await cls.validate_beneficiary_data(user_data)

        # create user in our database
        new_user = await ORMWrapper.create(Users, payload)
        new_user = new_user.__dict__  # convert object to dict
        return await rectify_payload(new_user)

    @classmethod
    async def update_user(cls, user_id: str):
        pass
        #  what details can't be updated, and how can update.

    @classmethod
    async def delete_user(cls, user_id: str):
        """
            Deleted user will be kept for 30 days, and then data will be
            removed after 30-days from a cron-job.
        """
        pass
