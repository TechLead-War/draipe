from asyncio.log import logger
from urllib.request import Request

from sanic import Blueprint

from contants import HTTPStatusCodes
from contants.exceptions import ExpectedDataNotFound
from managers.users import UserManager
from utils.parsers import send_response

password = Blueprint("password", url_prefix="/password")
email = Blueprint("email", url_prefix="/email")


@password.route("/forgot-password", methods=["POST"])
async def forgot_password(request: Request):
    email = request.json.get("email")
