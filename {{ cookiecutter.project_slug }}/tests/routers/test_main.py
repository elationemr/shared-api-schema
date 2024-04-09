from fastapi.testclient import TestClient


def test_get_root(test_client: TestClient) -> None:
    resp = test_client.get("/", follow_redirects=False)
    assert resp.status_code == 307
    assert "Location" in resp.headers
    assert resp.headers["Location"] == "/docs"
