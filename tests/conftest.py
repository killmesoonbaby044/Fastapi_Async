import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import app.routers.crud.base as base_crud

from app import models
from app.config import SettingsAD, SettingsLocal
from app.database import get_async_db
from app.models import Base, Post
from app.main import app
from app.oauth2 import create_access_token

settings_ad = SettingsLocal()


DATABASE_URL = (
    f"postgresql+asyncpg://{settings_ad.database_username}:{settings_ad.database_password}@"
    f"{settings_ad.database_hostname}/{settings_ad.database_name}_test"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    poolclass=NullPool,
)
TestingAsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture()
async def session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with TestingAsyncSessionLocal() as db:
        yield db


@pytest.fixture()
async def client(session):
    async def override_get_async_db():
        async with session as db:
            yield db

    app.dependency_overrides[get_async_db] = override_get_async_db
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as ac:
        yield ac


@pytest.fixture
async def test_user(client):
    user_data = {"email": "a@gmail.com", "password": "123!"}
    res = await client.post("/users", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
async def test_user2(client):
    user_data = {"email": "b@gmail.com", "password": "123!"}
    res = await client.post("/users", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
async def authorized_client(client, test_user):
    token = create_access_token(data={"user_id": test_user["id"]})
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
async def test_posts(test_user, session, test_user2):
    posts_data = [
        {"title": "1st title", "content": "first content", "owner_id": test_user['id']},
        {"title": "2nd title", "content": "2nd content", "owner_id": test_user['id']},
        {"title": "3rd title", "content": "3rd content", "owner_id": test_user['id']},
        {"title": "4th title", "content": "4rd content", "owner_id": test_user2['id']}
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    await session.commit()
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id'])])
    posts = await base_crud.get_table(session, Post)
    return posts.all()
