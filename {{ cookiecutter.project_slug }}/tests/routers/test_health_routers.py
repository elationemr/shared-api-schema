from typing import Generator
from unittest.mock import MagicMock, create_autospec

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.health_service import HealthException, HealthService


@pytest.fixture()
def mock_health_service() -> Generator:
    health_service = create_autospec(HealthService)
    app.dependency_overrides[HealthService] = lambda: health_service
    try:
        yield health_service
    finally:
        del app.dependency_overrides[HealthService]


def test_get_ready(mock_health_service: MagicMock, test_client: TestClient) -> None:
    mock_health_service.get_ready.return_value = True
    resp = test_client.get("/health/ready")
    assert resp.status_code == 204


def test_get_ready_returns_503_on_health_exception(
    mock_health_service: MagicMock, test_client: TestClient
) -> None:
    mock_health_service.get_ready.side_effect = HealthException("fake detail")
    resp = test_client.get("/health/ready")
    assert resp.status_code == 503
    assert resp.json() == {"detail": "fake detail"}


def test_get_ready_returns_503_on_unknown_exception(
    mock_health_service: MagicMock, test_client: TestClient
) -> None:
    mock_health_service.get_ready.side_effect = Exception("fake detail")
    resp = test_client.get("/health/ready")
    assert resp.status_code == 503
    assert resp.json() == {"detail": "An unexpected error has occurred"}


def test_get_live(mock_health_service: MagicMock, test_client: TestClient) -> None:
    mock_health_service.get_live.return_value = True
    resp = test_client.get("/health/live")
    assert resp.status_code == 204
