import re
from asyncio.log import logger
from datetime import datetime
from functools import wraps
from os import abort

import aiofiles
import requests
from sanic.request import Request

from contants.exceptions import InvalidTokenError, UserNotAuthorised
from context import user_tokens


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


async def block_bots(request: Request):

    # Defined a regular expression to match common bot user agents
    bot_regex = re.compile(r"(googlebot|bingbot|yandexbot|slurp)",
                           flags=re.IGNORECASE)

    # Check if the user agent matches the bot regex
    user_agent = request.headers.get('User-Agent')
    if user_agent and bot_regex.search(user_agent):
        logger.warning(f"Blocked bot with user agent: {user_agent}")
        abort()


# Decorator to authenticate the request
def authenticate(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        try:
            # Get the authorization header
            auth_header = request.headers.get("Authorization")

            if auth_header:
                # Extract the token from the header
                try:
                    token = ""
                    auth_header_parts = auth_header.split(" ")
                    if len(auth_header_parts) == 2 and auth_header_parts[0].lower() == "\"bearer":
                        token = auth_header_parts[1].strip('"')
                except ValueError:
                    raise UserNotAuthorised("Invalid authorization header")

                user_id = kwargs.get("user_id")
                user_token = user_tokens.get(user_id)
                if token == user_token:
                    # Token is valid, proceed with the request
                    return await func(request, *args, **kwargs)

            # No or invalid authorization header
            raise UserNotAuthorised("Invalid or missing token !!!")
        except ValueError:
            raise InvalidTokenError("Invalid format for token !!!")
    return wrapper
