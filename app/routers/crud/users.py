from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer

from .base import get_filter_row
from app.models import User
from app.exceptions.exception import UserExc


async def check_user_not_exist_by_email(
    db: AsyncSession, email: EmailStr
) -> HTTPException | None:
    user = await get_filter_row(db, User, email=email)
    if user:
        raise UserExc.http400()


async def get_user(db: AsyncSession, user_id):
    query = select(User).filter_by(id=user_id).options(defer(User.password))
    user = await db.scalar(query)
    return user


# user = await db.get(User, user_id)
#
#     if user is None:
#         raise UserExc.http404(user_id)
#
#     return user
