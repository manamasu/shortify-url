import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool
from app.api import app, get_session
from fastapi.testclient import TestClient

from app.models import URL


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


def test_delete_url(session: Session, client: TestClient):
    test_url = URL(
        title="TEST-TITLE-URL",
        long_url="https://sqlmodel.tiangolo.com/",
    )
    session.add(test_url)
    session.commit()

    response = client.delete(f"/api/v1/urls/{test_url.id}")

    url_in_db = session.get(URL, test_url.id)

    assert response.status_code == 200
    assert url_in_db is None
