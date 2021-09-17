from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .accounts import api as account_api
from .config import settings


app = FastAPI()
app.mount(settings.static_url, StaticFiles(directory=settings.static_directory), name='static')

account_api.initialize_app(app)