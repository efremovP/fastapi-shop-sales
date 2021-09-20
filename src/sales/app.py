from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .accounts import api as account_api
from .config import settings


app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie='session',
    max_age=100000
)
app.mount(settings.static_url, StaticFiles(directory=settings.static_directory), name='static')

account_api.initialize_app(app)