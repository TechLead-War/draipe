from asyncio.log import logger
import re
from os import abort
from datetime import datetime
from urllib.request import Request
import aiofiles
import requests


async def log_request(request: Request):
    """
        This functions logs all incoming request in request.log file.
    """
    async with aiofiles.open('request.log', 'a') as f:
        await f.write(f"Request method: {request.method}\n")
        await f.write(f"Request Host: {request.headers.get('Host')}\n")
        await f.write(f"Request URL: {request.url}\n")
        await f.write(f"Request headers: {request.headers}\n")
        await f.write(f"Request data: {request.json}\n")
        await f.write(f"Request time: {datetime.now()}\n\n")


async def block_bots(request):

    # Defined a regular expression to match common bot user agents
    bot_regex = re.compile(r"(googlebot|bingbot|yandexbot|slurp)",
                           flags=re.IGNORECASE)

    # Check if the user agent matches the bot regex
    user_agent = request.headers.get('User-Agent')
    if user_agent and bot_regex.search(user_agent):
        logger.warning(f"Blocked bot with user agent: {user_agent}")
        abort()
