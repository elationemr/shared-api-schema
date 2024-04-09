from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest
from el8.ext.fastapi.auth import InternalJWTBackend
from fastapi.testclient import TestClient
from starlette.middleware.authentication import AuthenticationMiddleware

from app.main import app


@pytest.fixture()
def test_client() -> Generator:
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def authenticated_test_client(test_client: TestClient) -> Generator:
    middleware: Any = app.middleware_stack
    while middleware and not isinstance(middleware, AuthenticationMiddleware):
        middleware = middleware.app

    assert isinstance(middleware.backend, InternalJWTBackend)
    internal_jwt_backend = middleware.backend

    test_client.headers["Authorization"] = "Bearer <fake-token>"

    with patch.object(
        internal_jwt_backend,
        "verify_and_decode_jwt",
        MagicMock(return_value={"scp": [], "practice_ids": [], "sub": "<test>"}),
    ):
        yield test_client
        internal_jwt_backend.verify_and_decode_jwt.assert_called_with("<fake-token>")
