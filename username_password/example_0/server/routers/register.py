import os
import hashlib
import binascii

from starlette.requests import Request
from starlette.responses import PlainTextResponse
from urllib.parse import parse_qs

import database

async def register(request: Request):
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