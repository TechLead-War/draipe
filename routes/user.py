from datetime import datetime
from urllib.request import Request

from asyncio.log import logger
from contants import UserStatus, Keys
from contants.messages import ErrorMessages
from managers.users import UserManager
from sanic import Blueprint
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

        # call manager to create object in 'Users' database
        result = await UserManager.create_user(data)
        return await send_response(result)

    except ValueError as ex:
        logger.error('Invalid data: %s', ex)

    except Exception as ex:
        logger.error(f"Exception occurred: {ex}")


# User login
@user.route('/login', methods=['POST'])
async def login(request: Request):
    payload = request.json  # Access the JSON payload
    username = payload.get('username')
    password = payload.get('password')

    # Validate username and password
    if username == 'admin' and password == 'password':
        # Successful login
        return send_response({'message': 'User logged in successfully'})
    else:
        # Invalid credentials
        return send_response({'message': 'Invalid username or password'}, status=401)


# User profile
@user.route('/profile/<user_id>', methods=['GET'])
async def profile(request: Request, user_id):
    # Retrieve user profile based on user_id
    # Handle logic to fetch user profile here
    return send_response({'user_id': user_id, 'name': 'John Doe', 'email': 'john@example.com'})


# Update user profile
@user.route('/profile/<user_id>', methods=['PUT'])
async def update_profile(request: Request, user_id):
    # Update user profile based on user_id
    # Handle logic to update user profile here
    return send_response({'message': 'User profile updated successfully'})


# Delete user profile
@user.route('/profile/<user_id>', methods=['DELETE'])
async def delete_profile(request: Request, user_id):
    # Delete user profile based on user_id
    # Handle logic to delete user profile here
    return send_response({'message': 'User profile deleted successfully'})