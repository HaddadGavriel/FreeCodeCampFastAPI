import pytest
from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    posts = response.json()

    posts_schemas = [schemas.PostVoteResponse(**post) for post in posts]

    assert response.status_code == 200
    assert len(posts) == len(test_posts)

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = response.json()
    post_schema = schemas.PostVoteResponse(**post)

    assert response.status_code == 200
    assert post_schema.Post.id == test_posts[0].id

def test_get_one_post_not_found(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/999999")
    assert response.status_code == 404
    
def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

@pytest.mark.parametrize("title, content, status_code", [
    ("New Post", "Content of the new post", 201),
    ("", "Content with empty title", 201),
    ("Title with empty content", "", 201),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, status_code):
    post_data = {"title": title, "content": content}
    response = authorized_client.post("/posts/", json=post_data)
    created_post = response.json()
    post_schema = schemas.PostResponse(**created_post)

    assert response.status_code == status_code
    if status_code == 201:
        assert post_schema.title == post_data["title"]
        assert post_schema.content == post_data["content"]
        assert post_schema.owner.id == test_user["id"]
        assert post_schema.owner.email == test_user["email"]
        assert post_schema.published

def test_unauthorized_user_create_post(client, test_posts):
    post_data = {"title": "Unauthorized Post", "content": "Content of the unauthorized post"}
    response = client.post("/posts/", json=post_data)
    assert response.status_code == 401

def test_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

def test_delete_post_not_found(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/999999")
    assert response.status_code == 404

def test_unauthorized_user_delete_post(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post_not_owner(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    updated_post_data = {"title": "Updated Title", "content": "Updated Content"}
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=updated_post_data)
    updated_post = response.json()
    post_schema = schemas.PostResponse(**updated_post)

    assert response.status_code == 200
    assert post_schema.title == updated_post_data["title"]
    assert post_schema.content == updated_post_data["content"]

def test_update_post_not_found(authorized_client, test_user, test_posts):
    updated_post_data = {"title": "Updated Title", "content": "Updated Content"}
    response = authorized_client.put(f"/posts/999999", json=updated_post_data)
    assert response.status_code == 404

def test_unauthorized_user_update_post(client, test_posts):
    updated_post_data = {"title": "Updated Title", "content": "Updated Content"}
    response = client.put(f"/posts/{test_posts[0].id}", json=updated_post_data)
    assert response.status_code == 401

def test_update_post_not_owner(authorized_client, test_user, test_posts):
    updated_post_data = {"title": "Updated Title", "content": "Updated Content"}
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=updated_post_data)
    assert response.status_code == 403

