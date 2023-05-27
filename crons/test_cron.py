import asyncio
import aiofiles
from datetime import datetime


async def test_cron():
    """
        This functions saves ping datetime in cron.log file.
    """
    async with aiofiles.open('cron.log', 'a') as f:
        await f.write(f"Cron method at: {datetime.now()}\n\n")


async def wrapper_fun():
    await test_cron()


# Create the event loop
loop = asyncio.get_event_loop()

# Run the wrapper function in the event loop
loop.run_until_complete(wrapper_fun())

# Close the event loop
loop.close()
