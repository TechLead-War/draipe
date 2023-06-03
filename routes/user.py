from asyncio.log import logger
from urllib.request import Request

from sanic import Blueprint
from sanic_jwt import protected

from contants import HTTPStatusCodes
from contants.exceptions import ExpectedDataNotFound, UserNotAuthorised
from contants.messages import ErrorMessages
from managers.users import UserManager
from utils.bots import authenticate
from utils.parsers import send_response, to_string

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
@user.route('/profile/delete/<user_id>', methods=['DELETE'])
@authenticate
async def delete_user(request: Request, user_id: str):
    # Delete user profile based on user phone number
    # Handle logic to delete user profile here
    """
        This route is protected using the @protected() decorator from Sanic
        JWT. This ensures that only authenticated users with a valid
        JWT token can access the route.
    """

    try:
        # call manager to create object in 'Users' database
        result = await UserManager.delete_user(user_id)
        return await send_response(data=result)

    except ExpectedDataNotFound as ex:
        logger.error('Invalid data: %s', ex)
        return await send_response(
            body={
                "response": "Proper payload not provided!",
                "status_code": HTTPStatusCodes.BAD_REQUEST.value
            }
        )


@user.route('/user/change_pass/<user_id>', methods=["PATCH"])
@authenticate
async def change_password(request: Request, user_id: str):
    data = request.json
    result = {
            "data": {
                "is_success": False,
                "description": ""
            },
            "status_code": ""
        }
    try:
        phone = data.get("phone")
        username = data.get("username")
        current_password = data.get("current_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        # password policy, also to be implemented.
        user_data = {
            "phone": phone,
            "username": username,
            "current_password": current_password,
            "new_password": new_password,
            "confirm_password": confirm_password
        }
        result = await UserManager.change_password(user_data)
        return await send_response(data=result["data"], status_code=result[
            "status_code"])

    except AttributeError:
        # when payload(data) is not given, in request
        result["data"]["description"] = ErrorMessages.PAYLOAD_INVALID.value
        return result


@user.route('/user/update_user', methods=["PATCH"])
async def update_user(request: Request):
    payload = request.json
    user_details = {
        "username": payload.get("username")
    }
    # correct the mapping
    payload.pop("username", None)
    result = await UserManager.update_user(user_details, payload)
    return await send_response(data=result["data"], status_code=result[
        "status_code"])


# User profile
@user.route('/profile/<user_id>', methods=['GET'])
async def get_user_profile(request: Request, user_id):
    # Retrieve user profile based on user_id
    # Handle logic to fetch user profile here

    result = await UserManager.get_user_details(user_id)
    return await send_response(data=to_string(result))

