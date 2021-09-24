from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from ..config import get_settings
from ..database import get_session
from ..exceptions import EntityDoesNotExistError
from .models import Shop
from .schemas import ShopCreate
from .schemas import ShopUpdate


class ShopService():
    def __init__(self, session=Depends(get_session), settings=Depends(get_settings)):
        self.session = session
        self.settings = settings

    # TODO удалить после тестов!!!
    def get_shops(self) -> List[Shop]:
        shops = self.session.execute(
            select(Shop)
        ).scalars().all()
        return shops

    def create_shop(self, shop_create: ShopCreate, account_id: int) -> Shop:
        shop = Shop(
            name=shop_create.name,
            account_id=account_id
        )
        self.session.add(shop)
        self.session.commit()

        return shop

    def update_shop(self, shop_id: int, shop_update: ShopUpdate, account_id: int) -> Shop:
        shop = self._get_shop(shop_id, account_id)
        shop.name = shop_update.name
        self.session.commit()

        return shop

    def delete_shop(self, shop_id: int, account_id: int):
        shop = self._get_shop(shop_id, account_id)
        self.session.delete(shop)
        self.session.commit()

    def get_shop(self, shop_id: int, account_id: int) -> Shop:
        shop = self._get_shop(shop_id, account_id)
        return shop

    def _get_shop(self, shop_id: int, account_id: int) -> Shop:
        try:
            shop = self.session.execute(
                select(Shop)
                .where(Shop.id == shop_id, Shop.account_id == account_id)
            ).scalar_one()
            return shop
        except NoResultFound:
            raise EntityDoesNotExistError from None
