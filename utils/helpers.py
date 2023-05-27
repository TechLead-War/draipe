import os
import re
import pytz
from tortoise import models
from models import Users
from datetime import date, datetime
from typing import Union
from sanic.log import logger


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
    return bool(re.match(phone_re, number))


async def is_email_or_phone_taken(email, phone_number):
    return await Users.filter(
        models.Q(email=email) | models.Q(phone_number=phone_number)
    ).exists()


def is_future_valid(check_time: str) -> bool:
    """
    This function checks whether a date is of future.
    i.e. check_time is greater than or equal to current time
    Args:
        check_time: corporate end time

    Returns: True or False

    """
    current_time = datetime.utcnow().replace(tzinfo=pytz.UTC)
    if check_time:
        converted_end_time = normalize_time(
            datetime.strptime(check_time, "%Y-%m-%d %H:%M:%S%z")
        )
        if converted_end_time <= current_time:
            return True
    return False


def convert_date_to_dd_mmm_yyyy_format(original_date: str) -> str:
    """
    This function convert date to DD MMM YYYY format
    Args:
        original_date: original date

    Returns: converted date

    """
    original_time = normalize_time(
        datetime.strptime(original_date, "%Y-%m-%d %H:%M:%S%z")
    )
    converted_date = original_time.strftime("%d %b %Y").upper()
    return converted_date


def get_no_of_days_from_current_time(original_time: str) -> int:
    """
    This function calculate no of days between current and provided date
    Args:
        original_time: datetime

    Returns: number of days

    """
    current_time = datetime.utcnow().replace(tzinfo=pytz.UTC)
    original_time = normalize_time(
        datetime.strptime(original_time, "%Y-%m-%d %H:%M:%S%z")
    )
    return (original_time - current_time).days


def is_current_time_in_range(
    start_time: Union[date, datetime], end_time: Union[date, datetime]
) -> bool:
    """
    This function performs check to validate if the current
    date lies inbetween start_date and end_date.
    Check can be used on dates and datetime object.

    Args:
        start_time: date or datetime object
        end_time: date or datetime object

    Returns:
        Boolean (True / False) data if valid returns True, else return False.

    Raises:
        TypeError: When correct datatype not correct.
    """
    try:
        current_time = None
        if isinstance(start_time, datetime):
            current_time = datetime.now()
        elif isinstance(start_time, date):
            current_time = date.today()
        return start_time <= current_time <= end_time

    except TypeError:
        logger.exception(
            f"Excepted values to be of date or datetime got "
            f"{type(start_time)} and {type(end_time)}."
        )
        return False


def convert_time(original_time: str) -> str:
    """
    This function converts time format from "HH:MM" to
    "H hours M minutes".
    Args:
        original_time: time to be converted

    Returns: converted time

    """
    converted_time = ""
    if original_time:
        original_time = original_time.split(":")
        if original_time[0] != "00":
            converted_time += original_time[0] + " " + "hours" + " "
        if original_time[-1] != "00":
            converted_time += original_time[-1] + " " + "minutes"
    return converted_time


def normalize_time(datetimeobj):
    """
    This function normalizes the datetime object or datetime
    string into UTC time format.
    Args:
        datetimeobj: datetime object.

    Returns:
        datetime object normalized to UTC time format.
    """
    return datetimeobj.astimezone(pytz.UTC)


def convert_to_datetimeobj(datetimestring: str):
    """
    This function converts the datetime string to
    datetime object.
    Args:
        datetimestring: datetime in string without time zone.

    Returns:
        datetime object without time zone.
    """
    converted_time = datetime.strptime(datetimestring, "%Y-%m-%d %H:%M:%S")
    return converted_time
