# Check if phone number if correct.
# check for valid email
import os
from datetime import datetime
from typing import re
from tortoise.query_utils import Q
import models
from models import Users


async def delete_local_temporary_files(file_path: str) -> None:
    """
    This function is responsible for deleting temporary files
    from local storage
    Args:
        file_path : local file path
    """
    if os.path.exists(file_path):
        os.remove(file_path)


def is_valid_dob(dob: str) -> bool:
    """

    Args:
        dob: date of birth of beneficiary

    Returns: True if dob is valid, False otherwise.

    """
    dob_format = "%Y-%m-%d"
    try:
        return bool(datetime.strptime(dob, dob_format))

    except ValueError:
        return False


def is_valid_gender(gender: str) -> bool:
    """
    This function validate the gender
    Args:
        gender: gender of beneficiary

    Returns: True if gender is valid, False otherwise.

    """
    allowed_genders = ["m", "f", "o"]
    if gender.lower() not in allowed_genders:
        return False
    return True


def is_valid_number(number: str) -> bool:
    """
    This function validates the phone number, the number should
    have 10 digits and should start from 2, 6, 7, 8 and 9.

    Args:
        number: phone number

    Returns: True or False

    """

    if not isinstance(number, str):
        number = str(number)
    phone_re = re.compile(r"^[26789]\d{9}$")
    return re.match(phone_re, number)


async def get_user_by_email_or_phone(email, phone_number):
    return await Users.get_or_none(models.Q(email=email) | models.Q(
        phone_number=phone_number))


async def is_email_or_phone_taken(email, phone_number):
    user = await get_user_by_email_or_phone(email, phone_number)
    return user is not None