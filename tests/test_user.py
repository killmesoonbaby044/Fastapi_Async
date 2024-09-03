import pytest
from jose import jwt
from app import schemas
from app.config import settings_ad


async def test_login_api(client, test_user):
    res = await client.post(
        "/login/api",
        json={"email": test_user["email"], "password": test_user["password"]},
    )
    assert res.status_code == 200

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token,
        settings_ad.secret_key,
        algorithms=[settings_ad.algorithm],
    )
    id = payload.get("user_id")

    assert id == test_user["id"]
    assert login_res.token_type == "bearer"


async def test_login_web(client, test_user):
    res = await client.post(
        "/login/web",
        data={"email": test_user["email"], "password": test_user["password"]}
    )
    assert res.status_code == 301

    token = res.cookies.get("token")[1:-1]
    scheme, _, param = token.partition(" ")
    payload = jwt.decode(
        param, settings_ad.secret_key, algorithms=[settings_ad.algorithm]
    )
    user_id = payload.get("user_id")

    assert user_id == test_user["id"]
    assert scheme == "Bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "123!", 403),
        ("a@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "123!", 422),
        ("a@gmail.com", None, 422),
    ],
)
async def test_incorrect_login_api(test_user, client, email, password, status_code):
    res = await client.post("/login/api", json={"email": email, "password": password})
    assert res.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "123!", 403),
        ("a@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "123!", 422),
        ("a@gmail.com", None, 422),
    ],
)
async def test_incorrect_login_web(test_user, client, email, password, status_code):
    res = await client.post("/login/web", data={"email": email, "password": password})
    assert res.status_code == status_code


async def test_create_user(client, session, authorized_client):
    res = await client.post("/users", json={"email": "aa@gmail.com", "password": "123!"})
    assert res.status_code == 201

    user = schemas.UserOut(**res.json())
    assert user.email == "aa@gmail.com"

    res = await authorized_client.get(f"/users/{user.id}")
    data = res.json()
    assert res.status_code == 200
    assert data["email"] == "aa@gmail.com"
    assert data["id"] == user.id
