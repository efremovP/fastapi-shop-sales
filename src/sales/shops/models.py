from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from ..database import Base


class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    account_id = Column(ForeignKey('accounts.id'), nullable=False)
    name = Column(String, nullable=False)
