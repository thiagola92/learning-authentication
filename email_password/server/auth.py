import base64
import hashlib
import binascii

from starlette.authentication import (
    AuthenticationBackend,
    AuthenticationError,
    AuthCredentials,
    SimpleUser,
)
from starlette.requests import HTTPConnection

from database import get_user_auth


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection):
        # No authroization, no access
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        scheme, credentials = auth.split()

        # Wrong authorization scheme
        if scheme.lower() != "basic":
            return

        # Extract email and password from credentials
        credentials = base64.b64decode(credentials)
        credentials = credentials.decode()
        email, _, password = credentials.partition(":")

        # Get real hash from database
        salt, hash = get_user_auth(email)
        if not salt or not hash:
            raise AuthenticationError("Invalid credentails")

        # Generate guess of hash
        password = password.encode()
        salt = binascii.a2b_hex(salt)
        guess = hashlib.scrypt(password, salt=salt, n=2, r=64, p=1)
        guess = binascii.b2a_hex(guess)
        guess = guess.decode()

        # Check if the hash guess is the same as real hash
        if hash != guess:
            raise AuthenticationError("Wrong password")

        return AuthCredentials(["authenticated"]), SimpleUser(email)