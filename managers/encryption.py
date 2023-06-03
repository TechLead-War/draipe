import secrets
import string

# please refer this page for password - https://pypi.org/project/password/


class Encryption:
    _password = ""

    @classmethod
    async def validate_password(cls, user_id: str, password: str):
        pass

    @classmethod
    async def create_password(cls, user_id: str):
        pass


def generate_bearer_token(length=32, include_symbols=False):
    # Define the characters to use for generating the token
    # Generates a bearer token of default length (32 characters)

    characters = string.ascii_letters + string.digits
    if include_symbols:
        characters += string.punctuation

    # Generate a random token using the specified length and characters
    token = ''.join(secrets.choice(characters) for _ in range(length))

    # Format the token as a bearer token
    bearer_token = f"Bearer {token}"
    return bearer_token
