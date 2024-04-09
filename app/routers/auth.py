from fastapi import APIRouter, Depends
from fastapi.params import Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette.templating import Jinja2Templates
from loguru import logger
from app.database import get_async_db
from app.routers.crud.auth import loging
from app.schemas import LoginUser

router = APIRouter(prefix="/login", tags=["login"])

templates = Jinja2Templates(directory="app/templates")


@router.post("/api")
async def api_login(user_cred: LoginUser, db: AsyncSession = Depends(get_async_db)):
    token = await loging(db, user_cred.email, user_cred.password)

    return {"token_type": "bearer", "access_token": token}


@router.get("")
async def get_web(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/web")
async def web_login(response: Response,
                    email: str = Form(...),
                    password: str = Form(...),
                    db: AsyncSession = Depends(get_async_db)
                    ):
    token = await loging(db, email, password)
    # token = "Bearer " + token
    response = RedirectResponse(url="/posts", status_code=status.HTTP_301_MOVED_PERMANENTLY)
    response.set_cookie(
        "token", f"Bearer {token}",
        httponly=True,
        max_age=36000,
        # expires=3600,
        # domain="localhost",
        # secure=False,
        samesite="strict")
    logger.info(f"User {email} logged in")
    return response


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("token")
    return RedirectResponse(url="/login/web")
