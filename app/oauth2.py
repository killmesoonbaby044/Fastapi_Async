from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_401_UNAUTHORIZED

from .routers.crud import users as user_crud
from app import schemas
from app.config import settings_local
from app.database import get_async_db

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
        user_id: int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


class OAuth2PasswordBearerCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        authorization_cookie = request.cookies.get("token")

        scheme, param = get_authorization_scheme_param(authorization)
        scheme_cookie, param_cookie = get_authorization_scheme_param(
            authorization_cookie
        )
        if not (authorization or scheme.lower() == "bearer") and not (
            authorization_cookie or scheme_cookie.lower() == "bearer"
        ):
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None

        return param or param_cookie


oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="login")


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
