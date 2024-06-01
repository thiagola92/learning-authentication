import os
import hashlib
import binascii
from urllib.parse import parse_qs

from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.authentication import AuthenticationError, AuthCredentials, SimpleUser

from database.user import get_user_auth
from database.cookie import save_credential


async def login(request: Request):
    # Refuse if not in the right format
    if request.headers.get("Content-Type") != "application/x-www-form-urlencoded":
        return PlainTextResponse("Invalid body format", 400)

    # Break down body
    body = await request.body()
    body = body.decode()
    fields = parse_qs(body)

    # Body must have username and password
    if "username" not in fields or "password" not in fields:
        return PlainTextResponse("Missing username or password", 400)

    # Get username and password
    username = fields["username"][0]
    password = fields["password"][0]

    # Get real hash from database
    salt, hash = get_user_auth(username)
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

    # Create a random credential
    credential = os.urandom(16)
    credential = binascii.b2a_hex(credential)

    # Save cookie credential
    save_credential(username, credential)

    # Return credential as cookie
    response = PlainTextResponse("Logged")
    response.set_cookie("username", username)
    response.set_cookie("credential", credential)
    return response
