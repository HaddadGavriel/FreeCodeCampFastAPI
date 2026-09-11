import pytest
from jose import jwt

from app.config import settings
from app import schemas



def test_create_user(client):
    response = client.post("/users/", json={"email": "testuser@example.com", "password": "testpassword"})

    user = schemas.UserResponse(**response.json())
    assert user.email == "testuser@example.com"
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post("/auth/login", data={"username": test_user["email"], "password": test_user["password"]})
    token = schemas.Token(**response.json())
    payload = jwt.decode(token.access_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])

    assert payload.get("user_id") == test_user["id"]
    assert token.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("testuser@example.com", "wrongpassword", 403),
    ("testuser@example.com", None, 422),
    ("wronguser@example.com", "testpassword", 403),
    (None, "testpassword", 422),
    ("nonexistent@example.com", "wrongpassword", 403),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post("/auth/login", data={"username": email, "password": password})
    assert response.status_code == status_code