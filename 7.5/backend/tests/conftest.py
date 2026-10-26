import os
os.environ["DATABASE_URL"] = "sqlite:///./test_retailops.db"
os.environ["JWT_SECRET_KEY"] = "pytest-secret-that-is-long-enough-for-tests-only"
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database import Base, engine

@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)
