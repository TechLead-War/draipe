import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.request import Request

from itsdangerous import URLSafeTimedSerializer
from sanic import Blueprint
from sanic.response import json

from contants.exceptions import (ExpiredTokenError, InvalidTokenError,
                                 UserNotFoundError)
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
email = Blueprint("email", url_prefix="/email")


class EmailWrapper:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def send_email(self, sender_email, recipient_email, subject, message,
                   attachments=None, cc=None, bcc=None):
        try:
            # Create a multipart/mixed MIME message
            msg = MIMEMultipart('mixed')
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject

            # Create a multipart/alternative MIME part
            alt_part = MIMEMultipart('alternative')
            msg.attach(alt_part)

            # Create the text and HTML versions of the email content
            text_part = MIMEText(message, 'plain')
            html_part = MIMEText(f'<html><body>{message}</body></html>', 'html')

            # Attach the text and HTML parts to the alternative part
            alt_part.attach(text_part)
            alt_part.attach(html_part)

            # Attach the file attachments, if provided
            if attachments:
                for attachment in attachments:
                    with open(attachment, 'rb') as file:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename="{attachment}"')
                    msg.attach(part)

            # Connect to the SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                # Start TLS encryption (if supported by the server)
                server.starttls()

                # Login to the SMTP server
                server.login(self.smtp_username, self.smtp_password)

                # Send the email
                server.sendmail(sender_email, recipient_email.split(','), msg.as_string())

            print('Email sent successfully!')

        except Exception as e:
            print(f'Failed to send email: {str(e)}')


class PasswordResetWrapper:
    async def forgot_password(self):
        """
            We generate a password reset token using the itsdangerous library and
            send it to the user's registered email address. The email contains a
            link to the password reset page with the token embedded in the URL.
            When the user visits the reset password page and submits the
            new password, we validate the token and update the user's password
            in the database.
        """

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

        # Update the user's password in the database
        # (replace with your own logic)

        # user = User.query.filter_by(email=email).first()
        # user.password = hash_password(new_password)
        # db.commit()

        return json({"message": "Password reset successful"})
