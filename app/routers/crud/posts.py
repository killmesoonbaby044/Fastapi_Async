from sqlalchemy import select, ScalarResult, func, Select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exception import PostExc
from app.models import Post, Vote


async def get_owner_posts(
    db: AsyncSession,
    user_id: int,
    limit: int = None,
    offset: int = None,
    title_contains: str = "",
):
    # query = select(PostSQL).where(PostSQL.owner_id == current_user.id).order_by(PostSQL.id)
    query: Select = (
        select(Post)
        .filter_by(owner_id=user_id)
        .limit(limit)
        .offset(offset)
        .filter(Post.title.contains(title_contains))
        .order_by(Post.id)
    )

    posts: ScalarResult = await db.scalars(query)
    return posts


async def get_post_table_with_vote(
    db: AsyncSession,
    offset: int = 0,
    title_contains: str = "",
    content_contains: str = "",
    limit: int = 50,
    post_id: int = None,
):
    # table = aliased(table, name="Post_test")
    query: Select = (
        select(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Post.id == Vote.post_id, isouter=True)
        .group_by(Post.id)
        .order_by(Post.id)
        .limit(limit)
        .offset(offset)
    )
    filters = []
    if post_id:
        filters.append(Post.id == post_id)
    if title_contains:
        filters.append(Post.title.contains(title_contains))
    if content_contains:
        filters.append(Post.content.contains(content_contains))

    if filters:
        query = query.filter(and_(*filters))

    # if post_id:
    #     query = query.filter(Post.id == post_id)
    # if title_contains != "":
    #     query = query.filter(Post.title.contains(title_contains))
    # if content_contains != "":
    #     query = query.filter(Post.content.contains(content_contains))

    response = await db.execute(query)
    # mapping is used for connecting names of table to rows of answer form this tables with relation
    posts = response.mappings()
    return posts


async def check_post_exist_and_permission(db: AsyncSession, post_id: int, user_id: int):
    post = await db.get(Post, post_id)

    if not post:
        raise PostExc.http404(post_id)

    if post.owner_id != user_id:
        raise PostExc.http403()

    return post


# async def get_filtered_join_table(
#         db: AsyncSession,
#         table: Type[Post | Vote | User],
#         join_table: Type[Post | Vote | User],
#         offset: int = None,
#         title_contains: str = "",
#         content_contains: str = "",
#         limit: int = None,
#         post_id: int = None
# ):
#     # table = aliased(table, name="Post_test")
#     query: Select = (
#         select(table, func.count(join_table.post_id).label("votes"))
#         .join(join_table, table.id == join_table.post_id, isouter=True)
#         .limit(limit)
#         .offset(offset)
#         .group_by(table.id)
#         .order_by(table.id)
#     )
#
#     if post_id:
#         query = query.filter(table.id == post_id)
#     if title_contains != '':
#         query = query.filter(table.title.contains(title_contains))
#     if content_contains != '':
#         query = query.filter(table.content.contains(content_contains))
#
#     response = await db.execute(query)
#     posts = response.mappings()
#     return posts
