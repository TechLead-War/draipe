from models import Users
from managers.orm_wrappers import ORMWrapper


async def fetch_record(filters: dict):
    user_details = await ORMWrapper.get_by_filters(
        Users, filters
    )
    user_details = user_details[0]
    return user_details
