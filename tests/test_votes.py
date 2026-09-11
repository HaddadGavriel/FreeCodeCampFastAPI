def test_vote_on_post(authorized_client, test_user, test_posts):
    vote_data = {"post_id": test_posts[0].id, "dir": 1}
    response = authorized_client.post("/vote/", json=vote_data)
    assert response.status_code == 201

def test_vote_on_post_twice(authorized_client, test_user, test_posts):
    vote_data = {"post_id": test_posts[0].id, "dir": 1}
    response = authorized_client.post("/vote/", json=vote_data)
    assert response.status_code == 201

    # Try to vote on the same post again
    response = authorized_client.post("/vote/", json=vote_data)
    assert response.status_code == 409  # Conflict status code

def test_delete_vote(authorized_client, test_user, test_posts):
    # First, vote on the post
    vote_data = {"post_id": test_posts[0].id, "dir": 1}
    response = authorized_client.post("/vote/", json=vote_data)
    assert response.status_code == 201

    # Now, delete the vote
    vote_data["dir"] = 0
    response = authorized_client.post("/vote/", json=vote_data)
    assert response.status_code == 201

def test_delete_vote_not_found(authorized_client, test_user, test_posts):
    vote_data = {"post_id": test_posts[0].id, "dir": 0}
    response = authorized_client.post("/vote/", json=vote_data)
    assert response.status_code == 404  # Not found status code

def test_unauthorized_vote(client, test_posts):
    vote_data = {"post_id": test_posts[0].id, "dir": 1}
    response = client.post("/vote/", json=vote_data)
    assert response.status_code == 401  # Unauthorized status code

def test_vote_on_nonexistent_post(authorized_client, test_user):
    vote_data = {"post_id": 999999, "dir": 1}  # Assuming this post ID does not exist
    response = authorized_client.post("/vote/", json=vote_data)
    assert response.status_code == 404  # Not found status code

    