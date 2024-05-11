import os
import hashlib
import binascii

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.requests import Request
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires

import database
from auth import AuthBackend


async def register(request: Request):
    # Refuse if not in the right format
    if request.headers.get("Content-Type") != "application/x-www-form-urlencoded":
        return PlainTextResponse("Invalid body format", 400)

    # Break down body
    body = await request.body()
    body = body.decode()
    parts = body.split("&")
    parts = [part.partition("=") for part in parts]

    # Get username and password
    username = ""
    password = ""
    for part in parts:
        if part[0] == "username":
            username = part[2]
        elif part[0] == "password":
            password = part[2]

    if not username or not password:
        return PlainTextResponse("Missing username or password", 400)

    # Found user with this username
    if database.get_user_auth(username)[0]:
        return PlainTextResponse("User already exist", 403)

    # Create salt and password hash
    salt = os.urandom(16)
    password = password.encode()
    hash = hashlib.scrypt(password, salt=salt, n=2, r=64, p=1)
    salt = binascii.b2a_hex(salt)
    hash = binascii.b2a_hex(hash)

    database.create_user(username, salt, hash)

    return PlainTextResponse("User created")


# Needs to be authenticated to receive this response
@requires("authenticated")
async def content(request: Request):
    return PlainTextResponse("Private content")


database.setup()

app = Starlette(
    debug=True,
    routes=[Route("/", content), Route("/register", register, methods=["post"])],
    middleware=[Middleware(AuthenticationMiddleware, backend=AuthBackend())],
)
