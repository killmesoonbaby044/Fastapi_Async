from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from app.oauth2 import create_access_token
from app.routers.crud.base import get_filter_row
from app.utils import pwd_context
from app.models import User
from loguru import logger


async def loging(request, db: AsyncSession, email, password):
    user = await get_filter_row(db, User, email=email)
    if not user:
        logger.warning(
            f"logging user doesnt exist -> {request.client.host!r} -> {request.headers['user-agent']!r} -> {email!r}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with this email not exists",
        )

    if not pwd_context.verify(password, user.password):
        logger.warning(
            f"Invalid Password -> {request.client.host!r} -> {request.headers['user-agent']!r} -> {email!r}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    token = create_access_token(data={"user_id": user.id})

    return token
