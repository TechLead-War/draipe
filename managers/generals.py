from contants.exceptions import DataInvalidOrNotFound
from managers.orm_wrappers import ORMWrapper
from models import Users


async def fetch_record(filters: dict, change_to_dict=False) -> dict:
    user_details = await ORMWrapper.get_by_filters(
        model=Users, filters=filters
    )

    if change_to_dict:
        user_details = user_details[0].__dict__

    if user_details:
        return user_details
    return {}


async def value_mapper(data: dict, mapping: dict) -> dict:
    # check if all required fields are present.
    resultant_user_data = dict()
    for key, value in mapping.items():
        if value.get("is_mandatory"):
            if not data.get(key, {}):
                raise DataInvalidOrNotFound(
                    f"Missing {key} in data!!"
                )
            else:
                resultant_user_data.update({
                    value["db_value"]: data[key]
                })
        else:
            raise DataInvalidOrNotFound(
                "Mapping given is not valid!!"
            )
    return resultant_user_data
