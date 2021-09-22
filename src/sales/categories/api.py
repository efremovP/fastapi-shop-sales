from typing import List

from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException

from .schemas import Category as CategorySchema
from .schemas import CreateCategory
from .schemas import UpdateCategory
from .service import CategoryService
from ..exceptions import EntityDoesNotExistError

router = APIRouter(
    prefix='/categories'
)


def initialize_app(app: FastAPI):
    app.include_router(router)


@router.get('', response_model=List[CategorySchema])
def get_categories(category_service: CategoryService = Depends()):
    categories = category_service.get_categories()
    return categories


@router.post(
    '',
    response_model=CategorySchema,
    status_code=status.HTTP_201_CREATED
)
def create_category(
        create_category: CreateCategory,
        category_service: CategoryService = Depends()
):
    category = category_service.create_category(create_category)

    return category


@router.patch(
    '/{category_id}',
    response_model=CategorySchema
)
def edit_category(
        category_id: int,
        category_update: UpdateCategory,
        category_service: CategoryService = Depends()
):
    try:
        category = category_service.update_category(category_id, category_update)
        return category
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None


@router.delete('/{category_id}')
def delete_category(
        category_id: int,
        category_service: CategoryService = Depends()
):
    try:
        category_service.delete_category(category_id)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND) from None
