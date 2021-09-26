from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..config import get_settings
from ..exceptions import EntityConflictError
from ..database import get_session
from .models import Operation
from ..shops.models import Shop
from ..categories.models import Category
from .schemas import OperationCreate
from .schemas import OperationGetParams
from ..shops.services import ShopService
from .report_service import Report


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

    def create_operation(self, operation_create: OperationCreate, account_id: int):
        operation = Operation(
            account_id=account_id
        )

        for k in operation_create.dict():
            setattr(operation, k, operation_create.dict()[k])

        self.session.add(operation)

        try:
            self.session.commit()
            return operation
        except IntegrityError:
            raise EntityConflictError() from None

    def chack_operation_param(
            self,
            operation_create: OperationCreate,
            account_id: int,
            shop_service: ShopService = Depends()
    ):
        try:
            shop_service.get_shop(operation_create.shop_id, account_id)
        except IntegrityError:
            raise EntityConflictError() from None

    def get_operations(self, get_params: OperationGetParams, account_id: int) -> List[Operation]:
        query = select(Operation)

        query = self._get_where_by_params(get_params, account_id, query)

        operations = self.session.execute(
            query
        ).scalars().all()

        return operations

    def get_report(self, get_params: OperationGetParams, account_id: int): # -> List[Operation]
        query = select(
            Operation.type,
            Operation.date,
            Shop.name.label("shop"),
            Category.name.label("category"),
            Operation.name,
            Operation.price,
            Operation.amount
        )
        query = query.join(Shop)
        query = query.outerjoin(Category)
        query = query.where(Operation.account_id == account_id)
        query = query.execution_options(yield_per=100)
        query = self._get_where_by_params(get_params, account_id, query)

        report = Report()
        for partition in self.session.execute(query).partitions(100):
            for row in partition:
                report.add_row(row)
                # print(f"{row.type} - {row.date} - {row.shop} - {row.category} - {row.name} - {row.price} - {row.amount}")

        return report.get_result()

    def _get_where_by_params(self, get_params: OperationGetParams, account_id: int, query):
        query.where(Operation.account_id == account_id)

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

        return query
