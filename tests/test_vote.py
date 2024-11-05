import pytest

from app.models import Vote


@pytest.fixture
async def test_vote(test_posts, session, test_user):
    new_vote = Vote(post_id=test_posts[0].id, user_id=test_user["id"])
    session.add(new_vote)
    await session.commit()


async def test_add_vote(authorized_client, test_posts):
    res = await authorized_client.post(
        "/votes", json={"post_id": test_posts[0].id, "dir": 1}
    )
    assert res.status_code == 201


async def test_remove_vote(authorized_client, test_posts, test_vote):
    res = await authorized_client.post(
        "/votes", json={"post_id": test_posts[0].id, "dir": 0}
    )
    assert res.status_code == 201


async def test_vote_twice(authorized_client, test_posts, test_vote):
    res = await authorized_client.post(
        "/votes", json={"post_id": test_posts[0].id, "dir": 1}
    )
    assert res.status_code == 409


async def test_delete_post_non_exist_vote(authorized_client, test_vote, test_posts):
    res = await authorized_client.post("/votes", json={"post_id": 66666, "dir": 0})
    assert res.status_code == 404


async def test_delete_vote_non_exist_post(authorized_client, test_posts):
    res = await authorized_client.post(
        "/votes", json={"post_id": test_posts[0].id, "dir": 0}
    )
    assert res.status_code == 404


async def test_delete_vote_non_authorized_user(client, test_posts):
    res = await client.post("/votes", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401
