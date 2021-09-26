from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import AccountLogin
from .schemas import AccountCreate
from .schemas import Token
from .services import AccountService
from ..exceptions import EntityConflictError
from ..exceptions import EntityDoesNotExistError

router = APIRouter(
    prefix='/sign'
)


def initialize_app(app: FastAPI):
    app.include_router(router)


@router.post('in', response_model=Token)
def login(
        credentials: OAuth2PasswordRequestForm = Depends(),
        service: AccountService = Depends()
):
    try:
        account_login = AccountLogin(
            username=credentials.username,
            password=credentials.password,
        )

        account = service.authenticate_account(account_login)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED) from None

    return service.create_tokens(account)


@router.post(
    'up',
    response_model=Token,
    status_code=status.HTTP_201_CREATED
)
def create_account(
        account_create: AccountCreate,
        service: AccountService = Depends()
):
    try:
        account = service.create_account(account_create)
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT) from None

    return service.create_tokens(account)
