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
from ..exceptions import EntityDoesNotExistError

router = APIRouter(
    prefix='/shops'
)

def initialize_app(app: FastAPI):
    app.include_router(router)

#TODO тестовая функция удалить!!!
@router.get('', response_model=List[ShopSchema])
def get_shops(
    shop_service: ShopService=Depends()
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
    shop_service: ShopService=Depends()
):
    shop = shop_service.create_shop(shop_create)
    return shop


@router.patch('/{shop_id}', response_model=ShopSchema)
def edit_shop(
        shop_id: int,
        shop_update: ShopUpdate,
        shop_service: ShopService=Depends()
):
    try:
        shop = shop_service.update_shop(shop_id, shop_update)
        return shop
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None

@router.delete('/{shop_id}')
def delete_shop(
        shop_id: int,
        shop_service: ShopService=Depends()
):
    try:
        shop_service.delete_shop(shop_id)
        return Response()
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None