import json
from functools import lru_cache

import boto3
import pytest
from httpx import AsyncClient

from integration import settings


@pytest.fixture()
def http_client() -> AsyncClient:
    auth_token = settings.API_AUTH_TOKEN
    if not auth_token:
        # Attempt to generate a token for the dev environment
        auth_token = get_dev_api_auth_token()

    return AsyncClient(
        base_url=settings.SERVICE_URL, headers={"Authorization": f"Bearer {auth_token}"}
    )


@lru_cache()
def get_dev_api_auth_token() -> str:
    """Generate an authentication token for the "dev" environment.
    Returns:
        str: The generated token
    """
    lambda_client = boto3.client("lambda", region_name="us-west-2")

    lambda_input = {
        "token": {
            "sub": "<test>",
            "scopes": ["test"],  # The lambda only allows the 'test' scope
            "claims": {"aud": "api://applications", "practice_ids": []},
        }
    }
    invoke_result = lambda_client.invoke(
        FunctionName="el8-dev-auth-internal-test-generate-token",
        Payload=json.dumps(lambda_input).encode("utf-8"),
    )

    payload = json.load(invoke_result["Payload"])
    assert "access_token" in payload
    return payload["access_token"]
