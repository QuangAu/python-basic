from datetime import timedelta
from typing import Optional
from uuid import UUID

import jwt
from common import utils
from common.exception import InValidLoginError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from schemas.client import Client
from schemas.user import User
from settings import JWT_ALGORITHM, JWT_SECRET
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

oa2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_access_token_by_user(user: User, expires: Optional[timedelta] = None):
    claims = {
        "sub": user.login_id,
        "id": str(user.id),
        "name": user.name,
        "is_admin": user.is_admin,
        "grant_type": "password"
    }

    expire = (
        utils.get_current_utc_time() + expires
        if expires
        else utils.get_current_utc_time() + timedelta(minutes=10)
    )
    claims.update({"exp": expire})

    return {"access_token":  jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM), "token_type": "bearer"}


def create_access_token_by_client(client: Client, expires: Optional[timedelta] = None):
    claims = {
        "sub": str(client.client_id),
        "scope": client.scopes,
        "grant_type": "client_credentials"
    }

    expire = (
        utils.get_current_utc_time() + expires
        if expires
        else utils.get_current_utc_time() + timedelta(minutes=10)
    )
    claims.update({"exp": expire})

    return {"access_token":  jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM), "token_type": "bearer"}


async def authenticate_user(username: str, password: str, db_context: AsyncSession):
    result = await db_context.scalars(
        select(User).filter(and_(User.login_id == username, User.is_active))
    )
    user = result.first()
    if not user:
        return False
    if utils.compare_hashed_text(password, user.password):
        return user


async def authenticate_client(client_id: str, client_secret: str, db_context: AsyncSession):
    result = await db_context.scalars(
        select(Client).filter(Client.client_id == UUID(client_id))
    )

    client = result.first()

    if not client:
        return False

    if utils.compare_hashed_text(client_secret, client.client_secret):
        return client


def token_interceptor(token: str = Depends(oa2_bearer)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        grant_type = payload.get("grant_type")
        match grant_type:
            case "password":
                user = User()
                user.login_id = payload.get("sub")
                user.id = UUID(payload.get("id"))
                user.name = payload.get("name")
                user.is_admin = payload.get("is_admin")
            case "client_credentials":
                user = User()
                user.login_id = "root"  # client_credentials authentication acts like root user
                user.is_admin = True
            case _:
                raise InValidLoginError
        return user
    except jwt.InvalidTokenError:
        raise InValidLoginError
        raise InValidLoginError
