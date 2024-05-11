import os
import hashlib
import binascii
import secrets
import smtplib
from email.message import EmailMessage

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
    # Break down body
    body = await request.body()
    body = body.decode()
    parts = body.split("&")
    parts = [part.partition("=") for part in parts]

    # Get email and password
    email = ""
    password = ""
    for part in parts:
        if part[0] == "email":
            email = part[2]
        elif part[0] == "password":
            password = part[2]

    if not email or not password:
        return PlainTextResponse("Missing email or password", 400)

    # Found user with this email
    if database.get_user_auth(email)[0]:
        return PlainTextResponse("User already exist", 403)

    # Create salt and password hash
    salt = os.urandom(16)
    password = password.encode()
    hash = hashlib.scrypt(password, salt=salt, n=2, r=64, p=1)
    salt = binascii.b2a_hex(salt)
    hash = binascii.b2a_hex(hash)

    database.create_user(email, salt, hash)

    return PlainTextResponse("User created")


async def recover_account(request: Request):
    # Get email in body
    email = await request.body()
    email = email.decode()

    # Didn't find user with this email
    if not database.get_user_auth(email)[0]:
        return PlainTextResponse("No account with this email", 403)

    # Create recovery code
    code = secrets.token_urlsafe(32)

    # Save to database, so we can check it later
    database.create_recovery_code(email, code)

    # Create email
    message = EmailMessage()
    message["Subject"] = "Recover account"
    message["From"] = "server@localhost"
    message["To"] = email
    message["Content"] = code

    # Send email
    s = smtplib.SMTP("localhost", 8025)
    s.send_message(message)
    s.quit()

    return PlainTextResponse("Recovery code sent to your email")


async def change_account(request: Request):
    # Break down body
    body = await request.body()
    body = body.decode()
    parts = body.split("&")
    parts = [part.partition("=") for part in parts]

    # Get email, recovery code and new password
    email = ""
    code = ""
    password = ""
    for part in parts:
        if part[0] == "email":
            email = part[2]
        elif part[0] == "code":
            code = part[2]
        elif part[0] == "password":
            password = part[2]

    if not email or not code or not password:
        return PlainTextResponse("Missing email/code/password", 400)

    if not database.is_recovery_code_valid(email, code):
        return PlainTextResponse("Invalid code", 403)

    # Create salt and new password hash
    salt = os.urandom(16)
    password = password.encode()
    hash = hashlib.scrypt(password, salt=salt, n=2, r=64, p=1)
    salt = binascii.b2a_hex(salt)
    hash = binascii.b2a_hex(hash)

    # Change password and remove recovery code
    database.change_account(email, salt, hash)
    database.delete_recovery_code(email)

    return PlainTextResponse("Password changed")


# Needs to be authenticated to receive this response
@requires("authenticated")
async def content(request: Request):
    return PlainTextResponse("Private content")


database.setup()

app = Starlette(
    debug=True,
    routes=[
        Route("/", content),
        Route("/register", register, methods=["post"]),
        Route("/recover_account", recover_account, methods=["post"]),
        Route("/change_account", change_account, methods=["post"]),
    ],
    middleware=[Middleware(AuthenticationMiddleware, backend=AuthBackend())],
)