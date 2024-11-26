import logging.config

from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from loguru import logger
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.database import engine
from app.logger import LOGGING_CONFIG
from app.routers import auth, users, posts, custom, votes
from app.sanitize import SanitizeMiddleware

app = FastAPI(title="PSYCHO")

# app.add_middleware(SanitizeMiddleware)


logging.config.dictConfig(LOGGING_CONFIG)


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError):
    error_messages = [
        f"Error: {error['msg']} -> Input: {error['input']} -> Expected: {error['loc'][-1]}"
        for error in exc.errors()
    ]
    logger.bind(file="RVE").error(f"Validation Errors: {list(enumerate(error_messages, 1))}")

    return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An internal server error occurred RVE",
            },
        )


# @app.exception_handler(ResponseValidationError)
# async def validation_exception_handler(request: Request, exc: ResponseValidationError):
#     error_messages = [
#         f"got: {error['input']} ->> instead: {error['loc'][2]} ->> {error['msg']}"
#         for error in exc.errors()
#     ]
#     logger.bind(file="RVE").error(error_messages)
#     return JSONResponse(
#         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         content={"detail": "RVE ERROR:(((( "}
#         # content={"detail": exc.errors(), "body": exc.body},
#     )


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
    return {"message": "Hello World"}
