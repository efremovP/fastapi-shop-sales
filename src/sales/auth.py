from typing import Optional
from datetime import datetime
from datetime import timedelta

from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel

from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/signin')

class Account(BaseModel):
    id: int
    email: str
    username: str

def create_token(account: Account, lifetime: int) -> str:
    now = datetime.utcnow()
    return jwt.encode({
        'sub': str(account.id),
        'exp': now + timedelta(seconds=lifetime),
        'iat': now,
        'nbf': now,
        'account': {
            'id': account.id,
            'email': account.email,
            'username': account.username,

        }
    }, settings.secret_key, 'HS256')

def get_current_account(token: str=Depends(oauth2_scheme)) -> Account:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Unauthorized user',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    token_data = jwt.decode(token, settings.secret_key, algorithms=['HS256'])

    if 'account' not in token_data:
        raise credentials_exception

    return Account(**token_data['account'])