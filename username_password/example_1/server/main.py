from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.requests import Request
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires

from database.setup import db_setup
from routers.register import register
from routers.login import login
from auth import AuthBackend


# Needs to be authenticated to receive this response
@requires("authenticated")
async def content(request: Request):
    return PlainTextResponse("Private content")


db_setup()

app = Starlette(
    debug=True,
    routes=[
        Route("/", content),
        Route("/register", register, methods=["post"]),
        Route("/login", login, methods=["post"]),
    ],
    middleware=[Middleware(AuthenticationMiddleware, backend=AuthBackend())],
)
