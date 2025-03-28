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


# the way we tell pytest what the fixture is, that we want it to be using has to have the exact name of the fixture.
# In this case, we named it client, so the parameter has to be exactly named client for it to work.
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

    res_data = response.json()

    assert res_data["id"] == 1
    assert res_data["title"] == "SQLModel-URL"
    assert res_data["long_url"] == "https://sqlmodel.tiangolo.com/"
    assert res_data["short_url"] is not None

    # Check if List of URLs are now exactly one
    response = client.get("/api/v1/urls")
    data = response.json()

    assert data == [res_data]


# the way we tell pytest what the fixture is, that we want it to be using has to have the exact name of the fixture.
# In this case, we named it session, so the parameter has to be exactly named session for it to work.
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
