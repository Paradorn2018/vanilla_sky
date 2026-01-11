from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from dotenv import load_dotenv
from pathlib import Path
import os
from fastapi.testclient import TestClient
from ..models import Todos, Users
import pytest
from ..routers.todos import get_current_user, get_db
from ..routers.auth import bcrypt_context

BASE_DIR = Path(__file__).resolve().parent  # TodoApp/
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_TEST_URL")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False},
    poolclass= StaticPool

)

TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base.metadata.create_all(bind = engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def make_override_get_user(user):
    def override_get_user():
        return {
            'username': user.username,
            'id': user.id,
            'user_role': 'admin'
        }
    return override_get_user


client = TestClient(app)

@pytest.fixture
def test_todo():

    db = TestingSessionLocal()

    db.execute(text("DELETE FROM todos"))
    db.execute(text("DELETE FROM users"))
    db.commit()

    user = Users(
        username="codingwithrobytest",
        email="test@test.com",
        hashed_password="fakepassword",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=user.id
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)

    # ใช้ dependency กลาง
    app.dependency_overrides[get_current_user] = make_override_get_user(user)

    yield db, todo, user
    db.close()


@pytest.fixture
def test_user():

    db = TestingSessionLocal()

    db.execute(text("DELETE FROM todos"))
    db.execute(text("DELETE FROM users"))
    db.commit()

    user = Users(
        username="codingwithroby",
        email="codingwithrobytest@email.com",
        first_name = "Eric",
        last_name = "Roby",
        hashed_password= bcrypt_context.hash("testpassword"),
        is_active=True,
        role = 'admin',
        phone_number = "(111)-111-111"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    app.dependency_overrides[get_current_user] = make_override_get_user(user)

    yield user
    db.close()