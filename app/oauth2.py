from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import APIKeyCookie
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import app.routers.crud.users as user_crud
from app import schemas
from app.OauthCookieBearer import OAuth2PasswordBearerCookie
from app.config import settings_local
from app.database import get_async_db

oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="login")
# cookie_scheme = APIKeyCookie(name="token")
SECRET_KEY = settings_local.secret_key
ALGORITHM = settings_local.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings_local.access_token_expire_minutes


def create_access_token(data: dict):
    data_to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_acc_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_async_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_acc_token(token, credentials_exception)
    user = await user_crud.get_user(db, token.id)
    return user


# async def get_current_user2(
#     token: str = Depends(cookie_scheme), db: AsyncSession = Depends(get_async_db)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail=f"Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     token = verify_acc_token(token, credentials_exception)
#     user = await user_crud.get_user(db, token.id)
#     return user
