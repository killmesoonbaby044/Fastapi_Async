import logging.config

from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.database import engine
from app.logger import LOGGING_CONFIG
from app.models import Base
from app.routers import auth, users, posts, custom, votes

app = FastAPI()

# app.add_middleware(SanitizeMiddleware)


logging.config.dictConfig(LOGGING_CONFIG)


logger.add(
    "response_validation.log",
    level="INFO",
    rotation="10 MB",
    enqueue=True,
    compression="zip",
    filter=lambda record: record["extra"]["file"] == "RVE",
)


# sys.stdout = LoguruStream()


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    error_messages = [
        f"got: {error['input']} ->> instead: {error['loc'][2]} ->> {error['msg']}"
        for error in exc.errors()
    ]
    logger.bind(file="RVE").error(error_messages)
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


@app.get("/")
async def root():
    print("as")
