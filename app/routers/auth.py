from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.routers.crud.base import get_filter_row
from app.database import get_async_db
from app.models import User
from app.oauth2 import create_access_token
from app.schemas import LoginUser
from app.utils import pwd_context

router = APIRouter(prefix="/login", tags=["login"])


@router.post("")
async def api_login(user_cred: LoginUser, db: AsyncSession = Depends(get_async_db)):
    user = await get_filter_row(db, User, email=user_cred.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with this email not exists",
        )

    if not pwd_context.verify(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials"
        )
    token = create_access_token(data={"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
