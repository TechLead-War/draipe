from datetime import datetime, timedelta
from functools import wraps

import jwt
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json

user = Blueprint("user")


# Secret key for JWT encoding and decoding
SECRET_KEY = "your_secret_key"


def generate_token(user_id):
    """
    Generate a JWT token for the user.
    """
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expiration time
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def protected():
    """
    Decorator to protect routes that require authentication.
    """
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            auth_header = request.headers.get("Authorization")

            if not auth_header or not auth_header.startswith("Bearer "):
                return json({"message": "Authorization header missing or invalid"}, status=401)

            token = auth_header.split("Bearer ")[1]

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                user_id = payload["user_id"]

                # Attach the user ID to the request for further processing
                request.ctx.user_id = user_id

            except jwt.ExpiredSignatureError:
                return json({"message": "Token expired"}, status=401)
            except (jwt.DecodeError, jwt.InvalidTokenError):
                return json({"message": "Invalid token"}, status=401)

            return await f(request, *args, **kwargs)

        return decorated_function

    return decorator


@user.route("/login", methods=["POST"])
async def login(request: Request):
    """
    User login endpoint.
    """
    # Simulated user authentication
    username = request.json.get("username")
    password = request.json.get("password")

    # Check if username and password are valid
    if username == "admin" and password == "password":
        # Generate JWT token
        token = generate_token(user_id=1)

        return json({"token": token})

    return json({"message": "Invalid username or password"}, status=401)


@user.route("/logout", methods=["POST"])
@protected()
async def logout(request: Request):
    """
    User logout endpoint.
    """
    # Perform logout operations, such as invalidating the token
    # You can also remove any user-specific data from the request context

    return json({"message": "Logged out successfully"})


@app.middleware("request")
async def token_invalid_check(request: Request):
    """
    Middleware to check if the token is invalid.
    """
    token = request.headers.get("Authorization", "").split(" ")[1]
    if token in token_invalidation_list:
        return json({"message": "Invalid token", "status": 401})

    return None


@app.route("/logout", methods=["POST"])
@jwt_required
async def logout(request: Request):
    """
    User logout endpoint.
    """
    token = get_raw_jwt(request)
    token_invalidation_list.add(token)
    # Perform any additional logout operations here, such as removing user-specific data

    return json({"message": "Logged out successfully"})


# Custom token invalidation list to store invalidated tokens
token_invalidation_list = set()


@jwt.expired_token_loader
async def expired_token_callback(request: Request):
    """
    Callback function to handle expired tokens.
    """
    token = get_raw_jwt(request)
    token_invalidation_list.add(token)
    return json({"message": "Token expired", "status": 401})


