"""
    This cron will work daily on 00:00hrs, and will delete all the users data
    that are requested to be deleted (user accounts).
"""

import asyncio
from datetime import datetime

import aiofiles


async def delete_users():
    """
        This functions deletes the user data and save action timestamp in
        cron.log file.
    """

    # writing delete logic here.

    async with aiofiles.open('cron.log', 'a') as f:
        await f.write(f"Cron method at: {datetime.now()}\n\n")


async def wrapper_fun():
    """
        maintaining this wrapper for future, if we need some use, or need to
        do some work, before executing the cron function.
    """
    await delete_users()


# Create the event loop
loop = asyncio.get_event_loop()

# Run the wrapper function in the event loop
loop.run_until_complete(wrapper_fun())

# Close the event loop
loop.close()
