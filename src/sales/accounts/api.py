from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile
from fastapi import HTTPException
from fastapi import status

from .schemas import Account as AccountSchema
from .schemas import AccountCreate
from .schemas import AccountUpdate
from .services import AccountService
from ..exceptions import EntityConflictError
from ..exceptions import EntityDoesNotExistError

router = APIRouter(
    prefix='/accounts'
)

def initialize_app(app: FastAPI):
    app.include_router(router)


@router.post(
    '',
    response_model=AccountSchema,
    status_code=status.HTTP_201_CREATED
)
def create_account(
        account_create: AccountCreate,
        service: AccountService = Depends()
):
    try:
        account = service.create_account(account_create)
        return account
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT) from None


@router.get('', response_model=List[AccountSchema])
def get_accounts(
    service: AccountService=Depends()
    ):
    return service.get_accounts()

@router.get('/{account_id}', response_model=AccountSchema)
def get_account(
        account_id: int,
        service: AccountService=Depends()
):
    try:
        return service.get_account(account_id)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None


@router.patch('/{account_id}', response_model=AccountSchema)
def edit_account(
        account_id: int,
        account_update: AccountUpdate,
        service: AccountService = Depends()
):
    try:
        account = service.update_account(account_id, account_update)
        return account
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None


@router.put('/{account_id}/avatar')
def update_account_avatar(
        account_id: int,
        avatar: UploadFile = File(...),
        service: AccountService = Depends()
):
    try:
        account = service.update_account_avatar(account_id, avatar)
        return account
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None