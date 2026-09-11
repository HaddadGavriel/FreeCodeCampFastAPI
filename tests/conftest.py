from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.database import get_db, Base
from app.main import app
from app.config import settings
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f"{settings.test_database_url}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_test_db

    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "testuser@example.com", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "testuser2@example.com", "password": "testpassword"}
    response = client.post("/users/", json=user_data)
    
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {"title": "First Post", "content": "Content of the first post", "owner_id": test_user["id"]},
        {"title": "Second Post", "content": "Content of the second post", "owner_id": test_user["id"]},
        {"title": "Third Post", "content": "Content of the third post", "owner_id": test_user["id"]},
        {"title": "Fourth Post", "content": "Content of the fourth post", "owner_id": test_user2["id"]},
        {"title": "Fifth Post", "content": "Content of the fifth post", "owner_id": test_user2["id"]},
    ]

    post_models = [models.Post(**post) for post in posts_data]
    session.add_all(post_models)
    session.commit()
    return session.query(models.Post).all()