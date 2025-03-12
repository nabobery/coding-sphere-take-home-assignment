import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
import sys
from pathlib import Path

# Add the project root directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from main import app
from core.db import get_session
from models.user import User
from core.security import get_password_hash
from models.project import Project

@pytest.fixture(name="client")
def client_fixture():
    # Create in-memory SQLite database for testing
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    
    # Override get_session dependency
    def get_test_session():
        with Session(engine) as session:
            yield session
    
    app.dependency_overrides[get_session] = get_test_session
    
    # Create test client
    client = TestClient(app)
    
    # Reset overrides after test is done
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="test_db")
def test_db_fixture():
    # Create in-memory SQLite database for testing
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session

@pytest.fixture(name="test_user")
def test_user_fixture(test_db: Session):
    # Create a test user
    user = User(
        username="testuser",
        email="testuser@example.com",
        full_name="Test User",
        role="user",
        hashed_password=get_password_hash("testpassword"),
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user

@pytest.fixture(name="test_admin")
def test_admin_fixture(test_db: Session):
    # Create a test admin
    admin = User(
        username="testadmin",
        email="testadmin@example.com",
        full_name="Test Admin",
        role="admin",
        hashed_password=get_password_hash("testpassword"),
    )
    test_db.add(admin)
    test_db.commit()
    test_db.refresh(admin)
    return admin

@pytest.fixture(name="test_project")
def test_project_fixture(test_db: Session, test_admin: User):
    # Create a test project
    project = Project(
        name="Test Project",
        description="A test project",
        owner_id=test_admin.id,
    )
    test_db.add(project)
    test_db.commit()
    test_db.refresh(project)
    return project