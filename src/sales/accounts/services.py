import shutil
from typing import List

from fastapi import Depends

from fastapi import Response
from fastapi import Request
from fastapi import UploadFile
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound

from ..config import PROJECT_ROOT
from ..config import get_settings
from ..exceptions import EntityConflictError
from ..exceptions import EntityDoesNotExistError
from ..database import get_session
from .models import Account
from .models import RefreshToken
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
        refresh_token = create_token(account, lifetime=self.settings.jwt_refresh_lifetime)

        try:
            account_token = self.session.execute(
                select(RefreshToken)
                .where(RefreshToken.account_id == account.id)
            ).scalar_one()
            account_token.token = refresh_token
        except NoResultFound:
            self.session.add(RefreshToken(
                account_id=account.id,
                token=refresh_token
            ))
        self.session.commit()

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type='bearer'
        )

    def get_accounts(self) -> List[Account]:
        accounts = self.session.execute(
            select(Account)
        ).scalars().all()

        return accounts

    def get_account_by_username(self, username: str) -> Account:
        try:
            account = self.session.execute(
                select(Account)
                .where(Account.username == username)
            ).scalar_one()
            return account
        except NoResultFound:
            raise EntityDoesNotExistError from None

    def get_account_by_refresh_token(self, token: str) -> Account:
        try:
            account = self.session.execute(
                select(Account)
                .join_from(Account, RefreshToken)
                .where(RefreshToken.token == token)
            ).scalar_one()
            return account
        except NoResultFound:
            raise EntityDoesNotExistError from None