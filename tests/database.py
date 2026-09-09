from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.database import get_db, Base
from app.main import app
from app.config import settings

SQLALCHEMY_DATABASE_URL = f"{settings.test_database_url}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def get_test_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_test_db

    yield TestClient(app)
