from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Vote


async def check_vote_exists(db: AsyncSession, user_id: int, post_id) -> int:
    query = select(
        exists().where(Vote.user_id == user_id).where(Vote.post_id == post_id)
    )
    existing = await db.scalar(query)
    return existing
