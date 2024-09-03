from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.database import get_async_db
from app.exceptions.exception import PostExc, VoteExc
from app.models import Vote, Post
from app.oauth2 import get_current_user
from app.routers.crud.base import add_row, delete_row, get_filter_row
from app.schemas import VoteIn

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_vote(
    data: VoteIn,
    db: AsyncSession = Depends(get_async_db),
    current_user: int = Depends(get_current_user),
):
    """check if post exist"""
    post = await db.get(Post, data.post_id)
    if not post:
        raise PostExc.http404(data.post_id)

    """check if vote exist"""
    vote = await get_filter_row(db, Vote, post_id=data.post_id, user_id=current_user.id)

    """dir=1 - adding vote, dir=0 - deleting vote"""
    if not vote:
        if data.dir == 1:
            await add_row(db, Vote(post_id=data.post_id, user_id=current_user.id))
            return {"message": "successfully added vote"}
        raise VoteExc.http404()

    elif vote:
        if data.dir == 0:
            await delete_row(db, vote)
            return {"message": "successfully deleted vote"}
        return VoteExc.http409(data.post_id, current_user.id)
