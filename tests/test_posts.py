from app import schemas
import pytest

data_no_publ = {
    "title": "NEW_SUPER_TITLE",
    "content": "NEW_SUPER_CONTENT"
}

data = {
    "title": "NEW_SUPER_TITLE",
    "content": "NEW_SUPER_CONTENT",
    "published": True
}


async def test_get_all_posts(authorized_client, test_posts):
    res = await authorized_client.get("/posts")

    # async def validate(post):
    #     return schemas.PostOut(**post)
    #
    # posts = map(validate, res.json())
    # posts_list = list(posts)
    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)


async def test_get_one_post(authorized_client, test_posts):
    res = await authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.owner_id == test_posts[0].owner_id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


async def test_unauthorized_get_posts(client, test_posts):
    res = await client.get("/posts")
    assert res.status_code == 401


async def test_unauthorized_get_one_post(client, test_posts):
    res = await client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


async def test_get_one_non_exist_post(authorized_client, test_posts):
    res = await authorized_client.get("/posts/8888888")
    assert res.status_code == 404


@pytest.mark.parametrize("title, content, published", [
    ("new_title", "new_content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
async def test_create_posts(authorized_client, test_user, title, content, published):
    res = await authorized_client.post('/posts', json={"title": title, "content": content, 'published': published})
    created_posts = schemas.PostBase(**res.json())
    assert res.status_code == 201
    assert created_posts.title == title
    assert created_posts.content == content
    assert created_posts.published == published
    assert created_posts.owner_id == test_user['id']


async def test_create_post_default_published_true(authorized_client, test_user):
    res = await authorized_client.post('/posts', json=data_no_publ)
    created_posts = schemas.PostBase(**res.json())
    assert res.status_code == 201
    assert created_posts.title == 'NEW_SUPER_TITLE'
    assert created_posts.content == 'NEW_SUPER_CONTENT'
    assert created_posts.published == True
    assert created_posts.owner_id == test_user['id']


async def test_unauthorized_user_create_post(client):
    res = await client.post("/posts", json=data)
    assert res.status_code == 401


async def test_unauthorized_user_delete_post(client, test_posts):
    res = await client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


async def test_delete_post_success(authorized_client, test_posts):
    res = await authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


async def test_delete_non_exist_post(authorized_client, test_posts):
    res = await authorized_client.delete("/posts/888888")
    assert res.status_code == 404


async def test_delete_other_user_post(authorized_client, test_posts, test_user, test_user2):
    res = await authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


async def test_update_post(authorized_client, test_posts, test_user):
    res = await authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_posts = schemas.PostBase(**res.json())
    assert res.status_code == 200
    assert updated_posts.title == data['title']
    assert updated_posts.content == data['content']
    assert updated_posts.published == data['published']


async def test_update_other_user_post(authorized_client, test_posts, test_user, test_user2):
    res = await authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


async def test_unauthorized_user_update_post(client, test_posts):
    res = await client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 401


async def test_update_non_exist_post(authorized_client, test_posts):
    res = await authorized_client.put("/posts/888888", json=data)
    assert res.status_code == 404
