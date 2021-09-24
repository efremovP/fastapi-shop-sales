from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .config import settings
from .accounts import api as account_api
from .shops import api as shop_api
from .categories import api as category_api
from .operations import api as operation_api

app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie='session',
    max_age=100000
)
app.mount(settings.static_url, StaticFiles(directory=settings.static_directory), name='static')

account_api.initialize_app(app)
shop_api.initialize_app(app)
category_api.initialize_app(app)
operation_api.initialize_app(app)
