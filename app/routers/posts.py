from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response

import app.routers.crud.base as base_crud
import app.routers.crud.posts as post_crud
from app.Query_Depends import post_query
from app.database import get_async_db
from app.exceptions.exception import PostExc
from app.models import Post, User
from app.oauth2 import check_token
from app.schemas import PostOut, PostBase, PostCreate

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("", status_code=status.HTTP_200_OK, response_model=List[PostOut])
async def get_posts(
    query: post_query,
    db: AsyncSession = Depends(get_async_db),
    user_id=Depends(check_token),
):
    posts = await post_crud.get_post_table_with_vote(db, **query)
    return posts.all()


@router.get("/my", response_model=List[PostBase], status_code=status.HTTP_200_OK)
async def get_my_posts(
    db: AsyncSession = Depends(get_async_db),
    user_id: int = Depends(check_token),
):
    posts = await post_crud.get_owner_posts(db, user_id)
    return posts.all()


@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostOut)
async def get_post_query_input(
    post_id: int,
    db: AsyncSession = Depends(get_async_db),
    user_id: int = Depends(check_token),
):
    result = await post_crud.get_post_table_with_vote(
        db=db,
        post_id=post_id,
        limit=1,
    )
    post = result.one_or_none()
    if not post:
        raise PostExc.http404(post_id)
    return post


@router.post("", response_model=PostBase, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_async_db),
    user_id: int = Depends(check_token),
):
    new_post = Post(**post.model_dump(), owner_id=user_id)
    updated_post = await base_crud.add_row(db, new_post)

    return updated_post


@router.put("/{post_id}", response_model=PostBase)
async def update_post(
    post_id: int,
    update_data: PostCreate,
    db: AsyncSession = Depends(get_async_db),
    user_id: int = Depends(check_token),
):
    post = await post_crud.check_post_exist_and_permission(db, post_id, user_id)

    updated_post = await base_crud.update_row(db, Post, post_id, update_data, post)

    return updated_post


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_async_db),
    user_id: int = Depends(check_token),
):
    post = await post_crud.check_post_exist_and_permission(db, post_id, user_id)

    await base_crud.delete_row(db, post)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
