from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, defaultload, defer
from starlette import status

from app.database import get_async_db
from app.models import Post, User
from app.oauth2 import get_current_user
from app.schemas import PostOut, UserOut

router = APIRouter(prefix="/custom", tags=["Custom"])


# with defaultload + defer you can choose what you should exclude from related and target table
@router.get(
    "/custom1",
    status_code=status.HTTP_200_OK,
)
async def get_custom_posts1(
    db: AsyncSession = Depends(get_async_db), current_user=Depends(get_current_user)
):
    query = select(Post).options(defaultload(Post.owner).defer(User.email))

    result = await db.scalars(query)
    post = result.all()

    return post


# choose what column you will request from database
@router.get("/custom2", status_code=status.HTTP_200_OK)
async def get_custom_posts2(
    db: AsyncSession = Depends(get_async_db), current_user=Depends(get_current_user)
):
    query = select(Post).options(load_only(Post.title)).filter_by(id=21)

    result = await db.scalars(query)
    post = result.one()
    return post


# You can use response_model_exclude only if you receive one object not a list
@router.get(
    "/custom3",
    response_model=PostOut,
    response_model_exclude={"published"},
    status_code=status.HTTP_200_OK,
)
async def get_custom_posts3(db: AsyncSession = Depends(get_async_db)):
    query = select(Post).filter_by(id=21).order_by(Post.id)
    result = await db.scalars(query)
    post = result.first()
    return post


@router.get("/custom4", status_code=status.HTTP_200_OK)
async def get_custom_posts4(db: AsyncSession = Depends(get_async_db)):
    # query = select(PostSQL).order_by(PostSQL.id)
    query = select(Post).filter_by(id=5).order_by(Post.id)
    result = await db.scalar(query)
    post = result
    return post
