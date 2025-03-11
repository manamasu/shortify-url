import os
import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from app.api import SessionDep, app, get_session
from fastapi.testclient import TestClient


# decorator on top of the function to tell pytest that this is a fixture function (equivalent to a FastAPI dependency).
@pytest.fixture(name="session")
# we create the custom engine, with the in-memory database, we create the tables, and we create the session.
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# the way we tell pytest what is the fixture that we want is by using the exact same name of the fixture.
# In this case, we named it session, so the parameter has to be exactly named session for it to work.
def test_get_urls(client: TestClient):

    # Check if we got no urls yet.
    response = client.get("/api/v1/urls")
    data = response.json()

    assert response.status_code == 200
    assert data == []

    # Post one URL and check for data

    response = client.post(
        "/api/v1/urls",
        json={"title": "SQLModel-URL", "long_url": "https://sqlmodel.tiangolo.com/"},
    )

    data = response.json()

    assert data == data

    assert data["title"] == "SQLModel-URL"
    assert data["long_url"] == "https://sqlmodel.tiangolo.com/"
    assert data["short_url"] == "https://shortExampleURL.com"

    # Check if List of URLs are now exactly one
    response = client.get("/api/v1/urls")
    data = response.json()

    assert data == [
        {
            "id": 1,
            "title": "SQLModel-URL",
            "long_url": "https://sqlmodel.tiangolo.com/",
            "short_url": "https://shortExampleURL.com",
        }
    ]
