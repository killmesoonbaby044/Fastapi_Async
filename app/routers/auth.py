from fastapi import APIRouter, Depends, Request, Response
from fastapi.params import Form
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse, HTMLResponse
from starlette.templating import Jinja2Templates
from app.routers.crud.auth import loging
from app.database import get_async_db
from app.schemas import LoginUser

router = APIRouter(prefix="/login", tags=["login"])

templates = Jinja2Templates(directory="app/templates")


@router.post("/api")
async def api_login(
    request: Request,
    user_cred: LoginUser,
    db: AsyncSession = Depends(get_async_db),
):
    token = await loging(request, db, user_cred.email, user_cred.password)
    logger.info(f"User {user_cred.email!r} logged in with api")
    return {"token_type": "bearer", "access_token": token}


@router.get("", response_class=HTMLResponse)
async def get_web(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/web")
async def web_login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_async_db),
):
    token = await loging(request, db, email, password)
    response = RedirectResponse(
        url="/posts", status_code=status.HTTP_301_MOVED_PERMANENTLY
    )
    response.set_cookie(
        "token",
        f"Bearer {token}",
        httponly=True,
        max_age=36000,
        # expires=3600,
        # domain="127.0.0.1",
        # secure=False,
        samesite="strict",
    )
    logger.info(f"User {email!r} logged in")
    return response


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("token")
    return RedirectResponse(url="/login/web")
