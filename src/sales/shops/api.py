from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Response

from .schemas import Shop as ShopSchema
from .schemas import ShopCreate
from .schemas import ShopUpdate
from .services import ShopService
from ..auth import Account
from ..auth import get_current_account
from ..exceptions import EntityDoesNotExistError

router = APIRouter(
    prefix='/shops'
)


def initialize_app(app: FastAPI):
    app.include_router(router)


# TODO тестовая функция удалить!!!
@router.get('')
def get_shops(
        shop_service: ShopService = Depends()
):
    shops = shop_service.get_shops()
    return shops


@router.post(
    '',
    response_model=ShopSchema,
    status_code=status.HTTP_201_CREATED
)
def create_shop(
        shop_create: ShopCreate,
        current_account: Account = Depends(get_current_account),
        shop_service: ShopService = Depends()
):
    shop = shop_service.create_shop(shop_create, current_account.id)
    return shop


@router.patch('/{shop_id}', response_model=ShopSchema)
def edit_shop(
        shop_id: int,
        shop_update: ShopUpdate,
        current_account: Account = Depends(get_current_account),
        shop_service: ShopService = Depends()
):
    try:
        shop = shop_service.update_shop(shop_id, shop_update, current_account.id)
        return shop
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None


@router.delete('/{shop_id}')
def delete_shop(
        shop_id: int,
        current_account: Account = Depends(get_current_account),
        shop_service: ShopService = Depends()
):
    try:
        shop_service.delete_shop(shop_id, current_account.id)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None
