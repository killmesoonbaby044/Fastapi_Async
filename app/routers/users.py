from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import app.routers.crud.base as base_crud
import app.routers.crud.users as user_crud
from app.database import get_async_db
from app.exceptions.exception import UserExc
from app.models import User
from app.oauth2 import get_current_user
from app.schemas import UserOut, UserCreate
from app.utils import hashing

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserOut], status_code=status.HTTP_200_OK)
async def get_users(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    users = await base_crud.get_table(db, User)
    return users.all()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user_cred: UserCreate, db: AsyncSession = Depends(get_async_db)):
    """
    In this function you can take two sides.
    First it's creating in pydantic model select request to DB and check if DB already have user with this email.
    Second - make insert request to db and catch with try except block IntegrityError in code.
    """
    await user_crud.check_user_not_exist_by_email(db, user_cred.email)
    user_cred.password = hashing(user_cred.password)
    new_user = User(**user_cred.model_dump())
    user = await base_crud.add_row(db, new_user)
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user),
):
    user = await user_crud.get_user(db, user_id)
    await base_crud.delete_row(db, user)

    return UserExc.http204(user_id)
