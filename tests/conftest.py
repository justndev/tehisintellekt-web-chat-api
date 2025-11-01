import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import Base


@pytest.fixture(scope='function')
def setup_test_database():
    """
    Sets up the test sqlite database and creates tables.
    """
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture(scope="session")
def client():
    return TestClient(app)