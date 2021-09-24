import enum

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import Enum
from sqlalchemy import DECIMAL
from sqlalchemy import ForeignKey

from ..database import Base

class TypeOperationEnum(enum.Enum):
    buy = 'buy'
    sale = 'sale'


class Operation(Base):
    __tablename__ = 'operations'

    id = Column(Integer, primary_key=True)
    account_id = Column(ForeignKey('accounts.id'), nullable=False)
    type = Column(Enum(TypeOperationEnum), nullable=False)
    date = Column(Date, nullable=False)
    shop_id = Column(ForeignKey('shops.id', ondelete='CASCADE'), nullable=False)
    category_id = Column(ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    # price = Column(DECIMAL(precision=10, scale=2, asdecimal=True), nullable=False)
    # amount = Column(DECIMAL(precision=10, scale=3, asdecimal=True), nullable=False)
