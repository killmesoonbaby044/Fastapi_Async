import sys

from loguru import logger
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.database import engine
from app.routers import auth, users, posts, custom, votes
from app.sanitize import SanitizeMiddleware

logger.add("app.log", rotation="10 MB", level="DEBUG", catch=True, enqueue=True, backtrace=True)
logger.add(sys.stdout, level="DEBUG")

app = FastAPI()

app.add_middleware(SanitizeMiddleware)


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    error = jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    # logger.error(str(error), exc_info=True, )
    print(error)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "RVE ERROR:(((( "}
        # content={"detail": exc.errors(), "body": exc.body},
    )


# @app.exception_handler(ResponseValidationError)
# async def validation_exception_handler(request: Request, exc: ResponseValidationError):
#
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
#     )

# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(custom.router)
app.include_router(votes.router)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
