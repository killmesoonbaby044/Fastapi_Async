from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exception import UserExc
from app.models import User
from app.routers.crud.base import get_filter_row


async def check_user_not_exist_by_email(db: AsyncSession, email: EmailStr):
    user = await get_filter_row(db, User, email=email)
    if user:
        raise UserExc.http400()


async def get_user(db: AsyncSession, user_id):
    user = await db.get(User, user_id)

    if user is None:
        raise UserExc.http404(user_id)

    return user
