from asyncio.log import logger
from urllib.request import Request

from sanic import Blueprint

from contants import HTTPStatusCodes
from contants.exceptions import ExpectedDataNotFound
from managers.users import UserManager
from utils.parsers import send_response

user = Blueprint("user")


@user.route("/ping/<name:str>", methods=['GET'])
@user.route("/ping", methods=['GET'], name='ping_route')
async def ping(request, name=''):
    """
        This is a demo route to test if service is running.

    """

    payload = request.args
    name = payload.get("name", name)
    name = f'Hello, {name}'

    return await send_response(data=name)


@user.route('/create/user', methods=['POST'])
async def create_user(request):
    """
       This route is responsible to create user in Users database.

    """

    try:
        data = request.json
        if not data:
            raise ExpectedDataNotFound("Payload is not provided!")
        # call manager to create object in 'Users' database
        result = await UserManager.create_user(data)
        return await send_response(data=result)

    except ExpectedDataNotFound as ex:
        logger.error('Invalid data: %s', ex)
        return await send_response(body={
            "response": "Proper payload not provided!",
            "status_code": HTTPStatusCodes.BAD_REQUEST.value})


# Delete user profile
@user.route('/profile/<user_id>', methods=['DELETE'])
async def delete_user(request: Request, number: str):
    # Delete user profile based on user phone number
    # Handle logic to delete user profile here

    try:
        # call manager to create object in 'Users' database
        result = await UserManager.delete_user(number)
        return await send_response(data=result)

    except ExpectedDataNotFound as ex:
        logger.error('Invalid data: %s', ex)
        return await send_response(
            body={
                "response": "Proper payload not provided!",
                "status_code": HTTPStatusCodes.BAD_REQUEST.value
            }
        )


@user.route('/user/change_pass', methods=["PATCH"])
async def change_password(request: Request):
    data = request.json

    phone = data.get("phone")
    username = data.get("username")
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    confirm_password = data.get("confirm_password")

    user_data = {
        "phone": phone,
        "username": username,
        "current_password": current_password,
        "new_password": new_password,
        "confirm_password": confirm_password
    }

    result = UserManager.change_password(user_data)
    return send_response(result)


@user.route('/user/change_pass', methods=["PATCH"])
async def update_user(request: Request):
    payload = request.json

    username = payload.get("username")

    new_payload = {key: value for key, value in payload.items()
                   if key != username}

    result = UserManager.change_password(username, new_payload)
    return send_response(result)


# User profile
@user.route('/profile/<user_id>', methods=['GET'])
async def get_user_profile(request: Request, user_id):
    # Retrieve user profile based on user_id
    # Handle logic to fetch user profile here

    result = await UserManager.get_user_details(user_id)
    return send_response(result)
