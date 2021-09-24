from typing import List
from typing import Optional
from datetime import date

from fastapi import FastAPI
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from ..exceptions import EntityConflictError
from .schemas import Operation as OperationSchema
from .schemas import OperationCreate
from .schemas import OperationGetParams
from .service import OperationService

router = APIRouter(
    prefix='/operations'
)


def initialize_app(app: FastAPI):
    app.include_router(router)

#TODO тестовая функция
@router.get('/all', response_model=List[OperationSchema])
def get_all_operations(
        operation_service: OperationService = Depends()
):
    operations = operation_service.get_all_operations()
    return operations

@router.get('', response_model=List[OperationSchema])
def get_operations(
        get_params: OperationGetParams = Depends(),
        operation_service: OperationService = Depends()
):
    operations = operation_service.get_operations(get_params)
    return operations

@router.get('/report')
def get_report(
        get_params: OperationGetParams = Depends(),
        operation_service: OperationService = Depends()
):
    operations = operation_service.get_report(get_params)
    return operations


@router.post(
    '',
    response_model=OperationSchema,
    status_code=status.HTTP_201_CREATED
)
def create_operation(
        operation_create: OperationCreate,
        operation_service: OperationService = Depends()
):
    try:
        operation = operation_service.create_operation(operation_create)
        return operation
    except EntityConflictError:
        # TODO добавить причину конфликта, нет такого магазина, нет такой категории
        raise HTTPException(status.HTTP_409_CONFLICT, detail="eeeeeee") from None

