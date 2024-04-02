from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.models import User
from app.oauth2 import create_access_token
from app.routers.crud.base import get_filter_row
from app.utils import pwd_context


async def loging(db: AsyncSession, email, password):
    user = await get_filter_row(db, User, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with this email not exists",
        )

    if not pwd_context.verify(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    token = create_access_token(data={"user_id": user.id})

    return token
