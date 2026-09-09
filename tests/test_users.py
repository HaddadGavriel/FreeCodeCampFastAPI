from app import schemas
from .database import client, session

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user(client):
    response = client.post("/users/", json={"email": "testuser@example.com", "password": "testpassword"})

    user = schemas.UserResponse(**response.json())
    assert user.email == "testuser@example.com"
    assert response.status_code == 201
