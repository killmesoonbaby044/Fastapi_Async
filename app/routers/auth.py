from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.database import get_async_db
from app.models import User
from app.oauth2 import create_access_token
from app.routers.crud.auth import loging
from app.routers.crud.base import get_filter_row
from app.schemas import LoginUser
from app.utils import pwd_context

router = APIRouter(prefix="/login", tags=["login"])

templates = Jinja2Templates(directory="app/templates")


@router.post("/api")
async def api_login(user_cred: LoginUser, db: AsyncSession = Depends(get_async_db)):
    token = await loging(db, user_cred.email, user_cred.password)

    return {"access_token": token, "token_type": "bearer"}


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
    response.set_cookie(
        "token", token,
        httponly=True,
        max_age=36000,
        # expires=3600,
        # domain="localhost",
        # secure=False,
        samesite="strict")
    return RedirectResponse(url="/home")


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("token")
    return RedirectResponse(url="/login/web")
