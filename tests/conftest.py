import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from application.quotes import app
from application.pms.database import Base, get_db
from application.pms import models
from application.pms.security import hash_password


@pytest.fixture
def test_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    db = TestingSessionLocal()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def teacher(test_db):
    user = models.User(
        name="Test Teacher",
        email="teacher@test.com",
        phone="9876543210",
        password_hash=hash_password("Teacher123"),
        role="teacher",
        status="active"
    )

    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    return user


@pytest.fixture
def student(test_db):
    user = models.User(
        name="Test Student",
        email="student@test.com",
        phone="9876543211",
        password_hash=hash_password("Student123"),
        role="student",
        status="active"
    )

    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    return user


@pytest.fixture
def teacher_token(client, teacher):
    response = client.post(
        "/auth/login",
        json={
            "email": "teacher@test.com",
            "password": "Teacher123"
        }
    )

    return response.json()["access_token"]


@pytest.fixture
def student_token(client, student):
    response = client.post(
        "/auth/login",
        json={
            "email": "student@test.com",
            "password": "Student123"
        }
    )

    return response.json()["access_token"]

