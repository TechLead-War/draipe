from sanic.response import json
from itsdangerous import URLSafeTimedSerializer
from email.mime.text import MIMEText
import smtplib
from sanic import Blueprint

from contants.exceptions import UserNotFoundError, InvalidTokenError, \
    ExpiredTokenError
from contants.keys import SMTPCredentials

# Secret key used for token generation
SECRET_KEY = SMTPCredentials.SECRET_KEY.value

# Configure email settings
SMTP_SERVER = SMTPCredentials.SMTP_SERVER.value
SMTP_PORT = SMTPCredentials.SMTP_PORT.value
SMTP_USERNAME = SMTPCredentials.SMTP_USERNAME.value
SMTP_PASSWORD = SMTPCredentials.SMTP_PASSWORD.value
SENDER_EMAIL = SMTPCredentials.SENDER_EMAIL.value

password = Blueprint("password", url_prefix="/password")


@password.route("/forgot-password", methods=["POST"])
async def forgot_password(request):
    """
        We generate a password reset token using the itsdangerous library and
        send it to the user's registered email address. The email contains a
        link to the password reset page with the token embedded in the URL.
        When the user visits the reset password page and submits the
        new password, we validate the token and update the user's password
        in the database.
    """

    email = request.json.get("email")

    # Generate a password reset token
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    token = serializer.dumps(email)

    # Compose the email
    reset_link = f"{SMTPCredentials.RESET_LINK.value}{token}"
    message = f"Click the following link to reset your password: {reset_link}"
    msg = MIMEText(message)
    msg["Subject"] = "Password Reset, Draipe."
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    try:
        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            smtp.send_message(msg)

        return json({"message": "Password reset link sent"})
    except Exception as e:
        return json({"error": str(e)}, status=500)


@password.route("/reset-password", methods=["POST"])
async def reset_password(request):
    token = request.json.get("token")
    new_password = request.json.get("password")

    # Validate the token
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        email = serializer.loads(token, max_age=3600)  # Token expires after 1 hour
        # Check if the user is found
        if user_not_found:
            raise UserNotFoundError("User not found")

        # Check if the token is invalid
        if invalid_token:
            raise InvalidTokenError("Invalid reset password token")

        # Check if the token has expired
        if expired_token:
            raise ExpiredTokenError("Reset password token has expired")

    except UserNotFoundError as e:
        return json({"error": str(e)}, status=404)

    except InvalidTokenError as e:
        return json({"error": str(e)}, status=400)

    except ExpiredTokenError as e:
        return json({"error": str(e)}, status=400)

    # Update the user's password in the database (replace with your own logic)
    # user = User.query.filter_by(email=email).first()
    # user.password = hash_password(new_password)
    # db.commit()

    return json({"message": "Password reset successful"})
