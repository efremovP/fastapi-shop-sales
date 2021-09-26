from typing import List

from fastapi import Depends

from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

from ..config import get_settings
from ..exceptions import EntityConflictError
from ..exceptions import EntityDoesNotExistError
from ..database import get_session
from .models import Account
from .schemas import AccountCreate
from .schemas import AccountLogin
from .schemas import Token
from ..auth import create_token


class AccountService():
    def __init__(self, session=Depends(get_session), settings=Depends(get_settings)):
        self.session = session
        self.settings = settings

    def create_account(self, account_create: AccountCreate) -> Account:
        account = Account(
            email=account_create.email,
            username=account_create.username,
            password=pbkdf2_sha256.hash(account_create.password)
        )
        self.session.add(account)
        try:
            self.session.commit()

            return account
        except IntegrityError:
            raise EntityConflictError from None

    def authenticate_account(self, account_login: AccountLogin) -> Account:
        try:
            account = self.session.execute(
                select(Account)
                .where(Account.username == account_login.username)
            ).scalar_one()
        except NoResultFound:
            raise EntityDoesNotExistError from None

        if not pbkdf2_sha256.verify(account_login.password, account.password):
            raise EntityDoesNotExistError from None

        return account

    def create_tokens(self, account: Account) -> Token:
        access_token = create_token(account, lifetime=self.settings.jwt_access_lifetime)

        return Token(
            access_token=access_token,
            token_type='bearer'
        )
