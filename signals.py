from typing import List, Type

from tortoise.signals import post_save

from models import Users


@post_save(Users)
async def post_save(
    sender: Type[Users],
    instance: Users,
    created: bool,
    using_db,
    update_fields: List[str],
) -> None:
    pass
