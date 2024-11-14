from typing import Type

from sqlalchemy import ScalarResult, select, update, Select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Post, User, Vote
from app.schemas import UserCreate, PostCreate


async def get_table(db: AsyncSession, table: Type[Post | User]) -> ScalarResult:
    query: Select = select(table)
    table_data = await db.scalars(query)
    return table_data


async def get_filter_row(db: AsyncSession, table, **kwargs):
    query: Select = select(table).filter_by(**kwargs)
    row = await db.scalar(query)
    return row


# def get_sync_filter_row(db: Session, table, **kwargs):
#     query: Select = select(table).filter_by(**kwargs).limit(1)
#     row = db.scalar(query)
#     return row


async def add_row(db: AsyncSession, data: Post | User | Vote):
    db.add(data)
    await db.commit()
    await db.refresh(data)
    return data


async def update_row(
    db: AsyncSession,
    table: Type[Post | User],
    row_id: int,
    data: PostCreate | UserCreate,
    row: Type[Post | User],
):
    update_query = update(table).filter_by(id=row_id).values(data.model_dump())

    await db.execute(update_query)
    await db.commit()
    await db.refresh(row)
    return row


async def delete_row(db: AsyncSession, row: Type[Post | User | Vote]):
    await db.delete(row)
    await db.commit()
