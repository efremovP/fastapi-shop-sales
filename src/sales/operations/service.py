from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..config import get_settings
from ..exceptions import EntityConflictError
from ..database import get_session
from .models import Operation
from .schemas import OperationCreate
from .schemas import OperationGetParams


class OperationService():
    def __init__(self, session=Depends(get_session), settings=Depends(get_settings)):
        self.session = session
        self.settings = settings

    # TODO только для тестов, удалить после тустирвания
    def get_all_operations(self) -> List[Operation]:
        operations = self.session.execute(
            select(Operation)
        ).scalars().all()
        return operations

    def create_operation(self, operation_create: OperationCreate):
        operation = Operation(
            account_id=1
        )

        for k in operation_create.dict():
            setattr(operation, k, operation_create.dict()[k])

        self.session.add(operation)

        try:
            self.session.commit()
            return operation
        except IntegrityError:
            raise EntityConflictError from None

    def get_operations(self, get_params: OperationGetParams) -> List[Operation]:
        operations = self._get_operations(get_params)

        return operations

    def get_report(self, get_params: OperationGetParams) -> List[Operation]:
        operations = self._get_operations(get_params)



        return operations

    def _get_operations(self, get_params: OperationGetParams) -> List[Operation]:
        query = select(Operation)

        if get_params.date_from:
            query = query.where(Operation.date >= get_params.date_from)

        if get_params.date_to:
            query = query.where(Operation.date <= get_params.date_to)

        if get_params.shops:
            shop_ids = get_params.shops.split(',')
            query = query.where(Operation.shop_id.in_(shop_ids))

        if get_params.categories:
            category_ids = get_params.categories.split(',')
            query = query.where(Operation.category_id.in_(category_ids))

        operations = self.session.execute(
            query
        ).scalars().all()
        return operations

