from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from ..config import get_settings
from ..database import get_session
from ..exceptions import EntityDoesNotExistError
from .models import Category
from .schemas import CreateCategory
from .schemas import UpdateCategory


class CategoryService():
    def __init__(self, session=Depends(get_session), settings=Depends(get_settings)):
        self.session = session
        self.settings = settings

    # TODO только для тестов, удалить после тустирвания
    def get_categories(self) -> List[Category]:
        categories = self.session.execute(
            select(Category)
        ).scalars().all()
        return categories

    def create_category(self, category_create: CreateCategory, account_id: int) -> Category:
        category = Category(
            name=category_create.name,
            account_id=account_id
        )
        self.session.add(category)
        self.session.commit()

        return category

    def update_category(self, category_id: int, category_update: UpdateCategory, account_id: int) -> Category:
        category = self._get_category(category_id, account_id)
        category.name = category_update.name
        self.session.commit()

        return category

    def delete_category(self, category_id: int, account_id: int):
        category = self._get_category(category_id, account_id)
        self.session.delete(category)
        self.session.commit()

    def get_category(self, category_id: int, account_id: int) -> Category:
        category = self._get_category(category_id, account_id)
        return category

    def _get_category(self, category_id: int, account_id: int) -> Category:
        try:
            category = self.session.execute(
                select(Category)
                .where(Category.id == category_id, Category.account_id == account_id)
            ).scalar_one()
            return category
        except NoResultFound:
            raise EntityDoesNotExistError from None
