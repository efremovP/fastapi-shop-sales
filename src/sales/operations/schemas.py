from typing import Optional
from datetime import date

from pydantic import BaseModel

from .models import TypeOperationEnum


class Operation(BaseModel):
    id: int
    type: TypeOperationEnum  # [buy, sale]
    date: date  # isodate
    shop_id: int
    category_id: Optional[int]
    name: str
    price: float
    amount: float

    class Config:
        orm_mode = True


class OperationCreate(BaseModel):
    type: TypeOperationEnum  # [buy, sale]
    date: date  # isodate
    shop_id: int
    category_id: Optional[int] = None
    name: str
    price: float
    amount: float

class OperationGetParams(BaseModel):
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    shops: Optional[str] = None
    categories: Optional[str] = None
