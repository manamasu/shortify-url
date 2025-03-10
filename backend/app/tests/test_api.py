from app.api import app
from starlette.testclient import TestClient

client = TestClient(app)


def test_get_urls():
    response = client.get("/api/v1/urls")
    assert response.status_code == 200
