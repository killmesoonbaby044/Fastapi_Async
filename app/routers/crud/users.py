from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer

from .base import get_filter_row
from app.models import User
from app.exceptions.exception import UserExc


async def get_user(db: AsyncSession, user_id):
    query = select(User).filter_by(id=user_id).options(defer(User.password))
    user = await db.scalar(query)
    return user


async def check_user_not_exists_by_email(
    db: AsyncSession, email: EmailStr
) -> HTTPException | None:
    query = select(exists().where(User.email == email))
    existing = await db.scalar(query)
    if existing:
        raise UserExc.http400()


async def check_user_exists_by_id(db: AsyncSession, user_id: int) -> int:
    query = select(exists().where(User.id == user_id))
    existing = await db.scalar(query)
    if existing:
        return user_id
    else:
        raise UserExc.http404(user_id)


# user = await db.get(User, user_id)
#
#     if user is None:
#         raise UserExc.http404(user_id)
#
#     return user
