from typing import Optional

from pydantic import BaseModel

class Account(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    username: str
    avatar: Optional[str]

    class Config:
        orm_mode=True

class AccountCreate(BaseModel):
    email: str
    username: str
    password: str

class AccountUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class AccountLogin(BaseModel):
    username: str
    password: str

class RefreshToken(BaseModel):
    token: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str