from typing import List

from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from ..exceptions import EntityConflictError
from ..exceptions import EntityDoesNotExistError
from .schemas import Operation as OperationSchema
from .schemas import OperationCreate
from .schemas import OperationGetParams
from .services import OperationService
from ..shops.services import ShopService
from ..categories.services import CategoryService

from ..auth import Account
from ..auth import get_current_account

router = APIRouter(
    prefix='/operations'
)


def initialize_app(app: FastAPI):
    app.include_router(router)


@router.post(
    '',
    response_model=OperationSchema,
    status_code=status.HTTP_201_CREATED
)
def create_operation(
        operation_create: OperationCreate,
        current_account: Account = Depends(get_current_account),
        operation_service: OperationService = Depends(),
        shop_service: ShopService = Depends(),
        category_service: CategoryService = Depends()
):
    try:
        shop_service.get_shop(operation_create.shop_id,  current_account.id)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Shop does not exist") from None

    try:
        if operation_create.category_id is not None:
            category_service.get_category(operation_create.category_id,  current_account.id)
    except EntityDoesNotExistError:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="Category does not exist") from None

    try:
        operation = operation_service.create_operation(operation_create, current_account.id)
        return operation
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=EntityConflictError.detail) from None


@router.get('', response_model=List[OperationSchema])
def get_operations(
        current_account: Account = Depends(get_current_account),
        get_params: OperationGetParams = Depends(),
        operation_service: OperationService = Depends()
):
    operations = operation_service.get_operations(get_params, current_account.id)
    return operations


@router.get('/report')
def get_report(
        current_account: Account = Depends(get_current_account),
        get_params: OperationGetParams = Depends(),
        operation_service: OperationService = Depends()
):
    operations = operation_service.get_report(get_params, current_account.id)
    return operations
