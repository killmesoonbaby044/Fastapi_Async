from fastapi import Query


async def post_query(
    limit: int = Query(None),
    offset: int = Query(None),
    title_contains: str = Query(""),
    content_contains: str = Query(""),
):
    return {
        "limit": limit,
        "offset": offset,
        "title_contains": title_contains,
        "content_contains": content_contains,
    }

#
# async def post_parameters(
#         limit: int = Query(None, alias="limit"),
#         offset: int = Query(None, alias="offset"),
#         title_contains: str = Query('', alias="title_contains"),
#         content_contains: str = Query('', alias="content_contains"),
# ):
#     query = {"limit": limit, "offset": offset, "title_contains": title_contains, "content_contains": content_contains}
#
#     return query
