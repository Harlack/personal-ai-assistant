from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base, get_session
from fastapi.testclient import TestClient
import pytest

@pytest.fixture
def client(clear_database):
    app.dependency_overrides[get_session] = override_get_session
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def override_get_session():
    session = TestSession()
    try:
        yield session
    finally:
        session.close()

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSession = sessionmaker(bind=test_engine)

@pytest.fixture
def clear_database():
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
